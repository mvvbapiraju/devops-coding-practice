# 02) Ci Secret Linter

## Question Context
Pre-merge check to prevent secret leakage in CI logs by scanning .gitlab-ci.yml scripts for sensitive env echo.

## Sample Inputs
```python
yaml_text = """
build:
  script:
    - echo $GITHUB_TOKEN
"""
```

## Expected Outputs
```python
[("build","echo $GITHUB_TOKEN")]
```

## Solution Approach
Parse YAML (fallback to line scan), detect print commands, and flag sensitive env var exposures.

## Complexity (why & how)
Linear in file size O(N); memory ~ number of hits.

## Code
```python
import re
_SENSITIVE_VAR = re.compile(r'\$(?:\{)?([A-Z0-9_]+)\}?')
_CMD = re.compile(r'(?i)\b(?:echo|printf|printenv)\b')

def _looks_sensitive(name):
    return (
        name.endswith('_TOKEN') or
        name.endswith('_SECRET') or
        name.endswith('_PASSWORD') or
        name.endswith('_KEY') or
        name.startswith('AWS_')
    )

def lint_ci_yaml(yaml_text):
    hits = []
    try:
        import yaml
        doc = yaml.safe_load(yaml_text) or {}
        for job, cfg in doc.items():
            if not isinstance(cfg, dict): 
                continue
            for line in (cfg.get('script') or []):
                s = str(line)
                if _CMD.search(s):
                    for m in _SENSITIVE_VAR.finditer(s):
                        if _looks_sensitive(m.group(1)):
                            hits.append((job, s))
                            break
    except Exception:
        for i, line in enumerate(yaml_text.splitlines(), 1):
            if _CMD.search(line):
                for m in _SENSITIVE_VAR.finditer(line):
                    if _looks_sensitive(m.group(1)):
                        hits.append((f"line:{i}", line))
                        break
    return hits
```
