# DevOps Coding Practice – Multi-Org CI

This repository hosts multiple “org tracks” (e.g., `Org1/`, `Org2/`, `Org3/`).  
Each org is a top-level folder containing structure as follows:
- `.github/workflows/ci.yml`
- `Org1/`
  - `run_ci.py` – how to compile and smoke-test for Org1
  - `requirements.txt` – Python deps for Org1
  - `exercises/`
  - `docs/`
- `Org2/`
  - `run_ci.py` – how to compile and smoke-test for Org2
  - `requirements.txt` – Python deps for Org2
  - `exercises/`
  - `docs/`
- `.idea/` (ignored by git)
- `LICENSE`, `.gitignore`


## How the CI works

**Workflow:** `.github/workflows/ci.yml`

1. **Prepare:** The `prepare` job scans top-level folders and treats any directory that contains **both** `run_ci.py` and `requirements.txt` as an **org**.
2. **Changed-org filter (default):** It diffs the current commit vs. base to find which **top-level org folders** changed and only runs those.
3. **CI change safety:** If a change touches only `.github/**`, the workflow automatically runs **all orgs** to validate the pipeline.
4. **Path filters:** Changes to the root `README.md` or `.idea/**` **do not** trigger the workflow.
5. **Matrix build:** For each selected org, the workflow:
  - sets up Python (3.12),
  - installs `pip` deps from `<org>/requirements.txt`,
  - runs `<org>/run_ci.py`.


## Manual override

Trigger the workflow from the **Actions** tab → **Run workflow** and choose:

- **Run Mode**
  - `changed` — only orgs with file changes (default)
  - `all` — run **every** discovered org
  - `custom` — run only a provided list
- **Custom Orgs** — when `custom` is selected, provide a comma/space-separated list (e.g., `Barclays, CGI`)


## Adding a new org

Create a new top-level folder, e.g. `Org3/`, with at least:
- `Org3/`
  - `run_ci.py`
  - `requirements.txt`
  - `exercises/`
  - `docs/`

Push your branch. The CI will automatically discover `Org3/`:
- If you modified `Org3/**`, it runs only `Org3`.
- If you modified only `.github/**`, it runs **all** orgs.
- If you want a full dry run, use **Run workflow → Run Mode: all**.


## Local development

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r Barclays/requirements.txt
python Barclays/run_ci.py
```
Replace Barclays with another org to test locally.

