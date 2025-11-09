# RedefinedHire AI — Onboarding MVP (Streamlit)

A minimal, deployable MVP to demo a "second screening" + onboarding plan generator for **RedefinedHire AI**.

## What it does
- **Candidate intake** (role, prior experience, skill self-ratings, concerns)
- **Self-efficacy pulse** (3 items)
- **Onboarding plan** with **small-wins** milestones (30/60/90), mentor & training suggestions
- **Risk flags** and **HITL** notes (no automated decisions)
- **Admin**-style parameters in sidebar (selection ratio, fairness checks are stubbed)

> This is a **rule-based mock** for demo purposes. No production model, no PII storage, and no vendor APIs are called.

---

## Run locally
```bash
# 1) Create a venv (optional)
python -m venv .venv && source .venv/bin/activate    # on Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Launch
streamlit run streamlit_app.py
```

Streamlit will print a local URL (e.g., http://localhost:8501) and a temporary public URL for sharing on your network.

---

## Deploy to Streamlit Community Cloud (free)
1. Create a **new GitHub repo** and upload all files from this folder.
2. Go to https://share.streamlit.io, **New app** → select your repo + branch.
3. **Main file:** `streamlit_app.py`
4. Click **Deploy**. You’ll get a live URL like `https://redefinedhireai.streamlit.app`.

> No secrets needed for this mock. If you later add APIs, set them in **Streamlit Secrets**.

---

## Deploy to Replit (also free)
1. Create a new **Python** Repl and upload these files.
2. In the shell, run:
   ```bash
   pip install -r requirements.txt
   streamlit run streamlit_app.py --server.port=8000 --server.address=0.0.0.0
   ```
3. Click the **"Open in a new tab"** icon; you’ll get a public URL like  
   `https://redefinedhireai.andykim.repl.co`.

---

## Customize the demo
- Adjust **score weights** and **milestones** in `streamlit_app.py` (search for `CONFIG`).
- Replace text blocks to match Maersk or Horizon/ContinuoCo language.
- Add a CSV of your competency model and map it in the `COMPETENCIES` section.

### Notes on governance
- No fully automated decisions (HITL required).
- No PII storage (everything stays in memory for the session).
- Fairness metrics are placeholders; wire up to real data for audits.

---

## License
MIT (demo use only)


---

## New Pages (Enhanced MVP)
- **📊 Fairness Dashboard:** Simulate and log AIR / 4-fifths checks. Exports a CSV.
- **📝 Recruiter Review Log:** HITL audit trail. Add session entries and export.

## Branding
- Streamlit theme (colors/typography) via `.streamlit/config.toml`.
