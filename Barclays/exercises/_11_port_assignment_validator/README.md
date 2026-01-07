# 11) Port Assignment Validator

## Question Context
Pre-provision guard for reserved/invalid ranges and service conflicts.

## Sample Inputs
```python
existing={8080:"web"}; requests=[(80,"web"),(8080,"api"),(70000,"svc")]
```

## Expected Outputs
```python
[(80,"web","root-only"),(8080,"api","conflict"),(70000,"svc","invalid")]
```

## Solution Approach
Apply rule checks per request; unchanged if same service keeps its port.

## Complexity (why & how)
O(n) time; O(1) extra memory.

## Code
```python
def validate_ports(existing, requests):
    out = []
    for p, svc in requests:
        if p < 1024:
            out.append((p, svc, "root-only"))
        elif p > 65535:
            out.append((p, svc, "invalid"))
        elif p in existing and existing[p] != svc:
            out.append((p, svc, "conflict"))
    return out
```
