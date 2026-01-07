# 10) Kms Policy Misuse Scan

## Question Context
Flag statements granting kms:* on * to non-approved principals.

## Sample Inputs
```python
policy={"Statement":[{"Action":"kms:*","Resource":"*","Principal":"*"}]}; allowed=set()
```

## Expected Outputs
```python
[{"Action":"kms:*","Resource":"*","Principal":"*"}]
```

## Solution Approach
Normalize lists and detect dangerous wildcard grants not in the allowlist.

## Complexity (why & how)
O(S×L) time; memory O(#offenders).

## Code
```python
def _as_list(x):
    return x if isinstance(x, list) else [x]

def kms_find_wildcards(policy, allowed=set()):
    bad = []
    for st in policy.get("Statement", []):
        acts = set(_as_list(st.get("Action", [])))
        res  = set(_as_list(st.get("Resource", [])))
        pr   = set(_as_list(st.get("Principal", [])))
        if "kms:*" in acts and "*" in res and not pr <= allowed:
            bad.append(st)
    return bad
```
