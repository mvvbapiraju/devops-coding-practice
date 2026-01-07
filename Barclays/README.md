# Barclays DevOps Interview Practice – Veera

This repository tracks hands-on coding exercises tailored for **Senior DevOps/Infrastructure Engineer ([JR-0000040557](https://www.linkedin.com/jobs/view/4311346220))** interviews.
It contains **12 practical drills** with real-world platform/SRE context, inputs/outputs, approach, complexity, and working Python solutions.

## Structure
- `exercises/NN_name/README.md` – context, sample inputs/outputs, approach, complexity
- `exercises/NN_name/solution.py` – working code
- `docs/barclays-context.md` – role & interview context
- `.github/workflows/ci.yml` – basic Python CI (syntax checks + a few smoke runs)
- `run_ci.py` – compile and sanity-run a subset of exercises
- `requirements.txt` – minimal deps (PyYAML for exercise #2)

## Quickstart
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# compile all solutions and run a few smoke tests
python run_ci.py
```

## Exercises
1. Log SLO Gate (p95 & error-rate per window)  
2. GitLab CI Secret Linter (YAML)  
3. Semantic Version Gate  
4. Blue/Green Cutover Planner  
5. Token Bucket Rate Limiter (per-user + global)  
6. K/V Config Deep-Merge with Protected Keys  
7. Access-Log Parser → Top Offenders  
8. Dead-Letter Triage (JSON)  
9. IaC Drift Detector  
10. KMS Policy Misuse Scan  
11. Port Assignment Validator  
12. Deployment Metrics Summarizer (DORA-ish)  

## How to create & push a new GitHub repo
```bash
# From this folder:
git init
git checkout -b main
git add .
git commit -m "Initial commit: Barclays DevOps interview practice pack"

# Create an empty repo on GitHub (web UI), then set the remote and push:
git remote add origin https://github.com/<your-username>/barclays-devops-practice.git
git push -u origin main
```
