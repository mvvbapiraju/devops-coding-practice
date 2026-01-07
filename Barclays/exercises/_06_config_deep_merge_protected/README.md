# 06) Config Deep Merge Protected

## Question Context
Compose base→env→runtime configs but deny overrides to protected key paths, recording violations.

## Sample Inputs
```python
base={"auth":{"client_id":"A","timeout":3},"svc":{"retries":2}}; env={"auth":{"client_id":"B"},"svc":{"retries":3}}; run={"svc":{"retries":4,"mode":"canary"}}; protected={("auth","client_id")}
```

## Expected Outputs
```python
merged={"auth":{"client_id":"A","timeout":3},"svc":{"retries":4,"mode":"canary"}}; violations=[("auth","client_id")]
```

## Solution Approach
Recursive merge with path-aware protection checks; later layers win unless protected.

## Complexity (why & how)
Visit each key once → O(total keys).

## Code
```python
def deep_merge(a, b, protected=set(), path=()):
    out = {} if a is None else dict(a)
    violations = []
    for k, v in (b or {}).items():
        p = path + (k,)
        if p in protected:
            violations.append(p)
            continue
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k], vs = deep_merge(out[k], v, protected, p)
            violations.extend(vs)
        else:
            out[k] = v
    return out, violations

def merge_config(base, env, runtime, protected):
    x, v1 = deep_merge(base, env, protected)
    y, v2 = deep_merge(x, runtime, protected)
    return y, (v1 + v2)
```
