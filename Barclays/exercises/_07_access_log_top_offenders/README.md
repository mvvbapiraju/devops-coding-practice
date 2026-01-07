# 07) Access Log Top Offenders

## Question Context
Identify top IPs and paths by 5xx since a given timestamp to target mitigations.

## Sample Inputs
```python
lines=[("10.0.0.5","2026-01-07T09:10:00Z",500,"/login")]; since=1736241000
```

## Expected Outputs
```python
([("10.0.0.5",1)],[("/login",1)])
```

## Solution Approach
Single pass filter + frequency tally with Counter.

## Complexity (why & how)
O(n) time; memory O(unique IPs + paths).

## Code
```python
from collections import Counter
from datetime import datetime, timezone

def _to_epoch(ts):
    if isinstance(ts, (int, float)): return int(ts)
    if isinstance(ts, str):
        s = ts.replace('Z', '+00:00')
        return int(datetime.fromisoformat(s).timestamp())
    raise ValueError("Unsupported ts")

def top_5xx(lines, since_epoch, k=5):
    ipc = Counter(); pathc = Counter()
    for ip, ts, status, path in lines:
        ep = _to_epoch(ts)
        if ep >= since_epoch and str(status).startswith("5"):
            ipc[ip] += 1
            pathc[path] += 1
    return ipc.most_common(k), pathc.most_common(k)
```
