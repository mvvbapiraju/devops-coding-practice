# 04) Blue Green Cutover

## Question Context
Recommend cutover when green remains healthy for an N-minute window; otherwise advise rollback.

## Sample Inputs
```python
events=[("2026-01-07T09:00:00Z","green",True,0.002,180),
        ("2026-01-07T09:10:05Z","green",True,0.002,195)]
```

## Expected Outputs
```python
"2026-01-07T09:10:05+00:00"
```

## Solution Approach
Sliding window, check thresholds when the window spans N minutes.

## Complexity (why & how)
O(n) time; window memory O(W).

## Code
```python
from collections import deque
from datetime import datetime, timezone

def _to_epoch(ts):
    if isinstance(ts, (int, float)): return int(ts)
    if isinstance(ts, str):
        s = ts.replace('Z', '+00:00')
        return int(datetime.fromisoformat(s).timestamp())
    raise ValueError("Unsupported ts")

def _iso(epoch):
    return datetime.fromtimestamp(int(epoch), tz=timezone.utc).isoformat()

def propose_cutover(events, window_minutes=10, err_max=0.01, p95_max=250, ok_ratio_min=0.999):
    W = window_minutes * 60
    dq = deque()
    ok_count = 0

    def window_ready(now):
        if not dq:
            return False
        if now - dq[0][0] < W:
            return False
        n = len(dq)
        ok_ratio = ok_count / n
        max_err = max(e[3] for e in dq)
        max_p95 = max(e[4] for e in dq)
        return ok_ratio >= ok_ratio_min and max_err <= err_max and max_p95 <= p95_max

    for ts, tgt, ok, err_rate, p95 in events:
        t = _to_epoch(ts)
        dq.append((t, tgt, ok, float(err_rate), float(p95)))
        ok_count += 1 if ok else 0
        while dq and (t - dq[0][0]) > W:
            _, _, old_ok, _, _ = dq.popleft()
            ok_count -= 1 if old_ok else 0
        if window_ready(t):
            return _iso(t)
    return "rollback"
```
