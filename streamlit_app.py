
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="RedefinedHire AI — Onboarding MVP", page_icon="✅", layout="wide")

# ---------------------------
# CONFIG
# ---------------------------
CONFIG = {
    "weights": {
        "experience_years": 0.20,
        "skill_avg": 0.35,
        "self_efficacy": 0.25,
        "confidence_in_tools": 0.20,
    },
    "thresholds": {
        "risk_low": 0.70,
        "risk_med": 0.50
    },
    "small_wins": [
        "Finish sandbox tasks with zero critical errors",
        "Shadow a peer for one full workflow and document steps",
        "Complete microlearning: 'Top 5 defects & how to prevent them'",
        "Close feedback loop with mentor (2 actionable next steps)",
        "Achieve first independent task sign-off"
    ],
    "roles": ["Logistics Coordinator", "Warehouse Associate", "Dispatcher", "Inventory Analyst", "Operations Lead"]
}

# ---------------------------
# HELPERS
# ---------------------------
def normalize_0_1(x, min_val, max_val):
    if max_val == min_val:
        return 0.0
    return float(np.clip((x - min_val) / (max_val - min_val), 0.0, 1.0))

def score_candidate(inputs):
    # Basic normalization + weighted sum
    exp = normalize_0_1(inputs["experience_years"], 0, 10)
    skill_avg = float(np.mean(list(inputs["skills"].values())) / 5.0)  # 1-5 scale -> 0-1
    self_efficacy = float(np.mean(inputs["self_efficacy"]) / 5.0)
    tool_conf = float(inputs["confidence_in_tools"] / 5.0)
    
    w = CONFIG["weights"]
    composite = (
        w["experience_years"] * exp +
        w["skill_avg"] * skill_avg +
        w["self_efficacy"] * self_efficacy +
        w["confidence_in_tools"] * tool_conf
    )
    return float(composite)

def risk_band(score):
    if score >= CONFIG["thresholds"]["risk_low"]:
        return "Low", "green"
    if score >= CONFIG["thresholds"]["risk_med"]:
        return "Medium", "orange"
    return "High", "red"

def make_plan(inputs, score):
    band, _ = risk_band(score)
    role = inputs["role"]
    wins = CONFIG["small_wins"]
    concerns = inputs["concerns"]
    # Personalize small wins based on concern keywords
    if "accuracy" in concerns.lower():
        chosen = [wins[0], wins[2], wins[4]]
    elif "speed" in concerns.lower():
        chosen = [wins[1], wins[3], wins[4]]
    else:
        chosen = wins[:3] + wins[-1:]
    
    # Build a 30/60/90 plan
    plan = {
        "30": [
            f"Complete role-based onboarding for {role}",
            f"Small win: {chosen[0]}",
            "Meet assigned mentor; set 2 developmental goals"
        ],
        "60": [
            f"Small win: {chosen[1]}",
            "Shadow → run one full task end-to-end with mentor sign-off",
            "Microlearning module 2 + knowledge check ≥ 80%"
        ],
        "90": [
            f"Small win: {chosen[2]}",
            "Operate independently on core tasks; defect rate ≤ team median",
            "Retrospective with manager; set next-quarter growth plan"
        ]
    }
    if band == "High":
        plan["30"].append("Weekly check-ins with manager (15 min)")
        plan["60"].append("Pair-work twice per week to reinforce skills")
    return plan

def plan_to_df(plan_dict):
    rows = []
    for horizon, items in plan_dict.items():
        for idx, item in enumerate(items, start=1):
            rows.append({"Horizon": horizon, "Step": idx, "Milestone / Action": item})
    return pd.DataFrame(rows)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.header("Admin Controls (Demo)")
st.sidebar.caption("These affect only the mock scoring.")
with st.sidebar.expander("Weights"):
    w_exp = st.sidebar.slider("Experience (yrs)", 0.0, 1.0, CONFIG["weights"]["experience_years"], 0.05)
    w_skill = st.sidebar.slider("Skill Average", 0.0, 1.0, CONFIG["weights"]["skill_avg"], 0.05)
    w_efficacy = st.sidebar.slider("Self-efficacy", 0.0, 1.0, CONFIG["weights"]["self_efficacy"], 0.05)
    w_tools = st.sidebar.slider("Confidence in Tools", 0.0, 1.0, CONFIG["weights"]["confidence_in_tools"], 0.05)
    total = w_exp + w_skill + w_efficacy + w_tools
    if abs(total - 1.0) > 1e-6:
        st.sidebar.warning(f"Weights must sum to 1.0 (current = {total:.2f})")
    CONFIG["weights"].update({
        "experience_years": w_exp,
        "skill_avg": w_skill,
        "self_efficacy": w_efficacy,
        "confidence_in_tools": w_tools
    })

with st.sidebar.expander("Risk thresholds"):
    CONFIG["thresholds"]["risk_low"] = st.slider("Low risk ≥", 0.5, 0.95, CONFIG["thresholds"]["risk_low"], 0.01)
    CONFIG["thresholds"]["risk_med"] = st.slider("Medium risk ≥", 0.3, 0.9, CONFIG["thresholds"]["risk_med"], 0.01)

st.sidebar.markdown("---")
st.sidebar.subheader("Demo Notes")
st.sidebar.write("• No PII stored. • No automated decisions. • Fairness checks TBD.")

# ---------------------------
# MAIN
# ---------------------------
st.title("RedefinedHire AI — Onboarding MVP")
st.caption("Second screening → self-efficacy pulse → small-wins 30/60/90 plan (HITL required)")

col1, col2 = st.columns([1.2, 1])
with col1:
    st.subheader("Candidate Intake")
    role = st.selectbox("Target role", CONFIG["roles"], index=0)
    experience_years = st.number_input("Years of relevant experience", min_value=0.0, max_value=40.0, value=1.0, step=0.5)
    skills = {
        "Process knowledge": st.slider("Process knowledge (1–5)", 1, 5, 3),
        "Quality focus": st.slider("Quality focus (1–5)", 1, 5, 3),
        "Throughput/Speed": st.slider("Throughput/Speed (1–5)", 1, 5, 3),
        "Systems/Tools": st.slider("Systems/Tools (1–5)", 1, 5, 3),
    }
    confidence_in_tools = st.slider("Confidence with tools/workflow (1–5)", 1, 5, 3)
    concerns = st.text_input("Biggest concern in first 30 days (free text)", placeholder="e.g., accuracy, speed, tools")

with col2:
    st.subheader("Self-efficacy Pulse (1–5)")
    se1 = st.slider("I can master the core tasks for this role.", 1, 5, 3)
    se2 = st.slider("I can learn from early mistakes and improve.", 1, 5, 3)
    se3 = st.slider("I can leverage support (mentor/peers) effectively.", 1, 5, 3)

    if st.button("Generate Plan"):
        inputs = {
            "role": role,
            "experience_years": experience_years,
            "skills": skills,
            "confidence_in_tools": confidence_in_tools,
            "self_efficacy": [se1, se2, se3],
            "concerns": concerns or ""
        }
        score = score_candidate(inputs)
        band, color = risk_band(score)

        st.markdown(f"### Composite Readiness: **{score:.2f}** — :{color}[{band} Risk]")
        plan = make_plan(inputs, score)
        df = plan_to_df(plan)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.download_button(
            label="Download 30/60/90 Plan (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="RedefinedHireAI_30-60-90_plan.csv",
            mime="text/csv"
        )

st.markdown("---")
st.subheader("Governance & Notes")
st.markdown("""
- **HITL:** Managers must review and adapt recommendations. No automated decisions.
- **Small wins:** Early, achievable milestones build self-efficacy and reduce anxiety.
- **Data:** No PII stored; all data is session-only.
- **Fairness:** This demo does not compute AIR/4-fifths. In production, integrate fairness auditing and adverse-impact monitoring.
""")

st.info("Tip: Use the sidebar to tweak weights and thresholds during stakeholder demos.")
