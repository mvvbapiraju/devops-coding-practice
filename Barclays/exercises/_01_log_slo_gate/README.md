# 01) Log Slo Gate

## Question Context
Gate promotions by flagging 5-minute windows where error-rate or p95 latency exceed SLO thresholds.

## Sample Inputs
```python
rows=[("2026-01-07T09:00:01Z","auth","OK",210),
      ("2026-01-07T09:02:50Z","auth","ERROR",1300)]
```

## Expected Outputs
```python
[("2026-01-07T09:00:00+00:00",0.5,1300)]
```

## Solution Approach
Bucket rows by window; compute error rate and p95; emit breaches.

## Complexity (why & how)
Build O(n); worst-case O(n log n) for per-bucket sort; space O(n).

## Code
```python
from datetime import datetime, timezone
import math

def _to_epoch(ts):
    if isinstance(ts, (int, float)): return int(ts)
    if isinstance(ts, str):
        s = ts.replace('Z', '+00:00')
        return int(datetime.fromisoformat(s).timestamp())
    raise ValueError("Unsupported ts")

def _iso(epoch):
    return datetime.fromtimestamp(int(epoch), tz=timezone.utc).isoformat()

def slo_breaches(rows, window_sec=300, p95_ms=250, err_thresh=0.01):
    buckets = {}
    for ts, service, status, latency_ms in rows:
        ep = _to_epoch(ts)
        bstart = (ep // window_sec) * window_sec
        b = buckets.setdefault(bstart, {"lats": [], "tot": 0, "err": 0})
        b["lats"].append(int(latency_ms))
        b["tot"] += 1
        is_ok = (str(status).isdigit() and int(status) < 400) or status == "OK"
        b["err"] += 0 if is_ok else 1

    out = []
    for bstart, info in sorted(buckets.items()):
        n = info["tot"]
        if n == 0:
            continue
        lats = sorted(info["lats"])
        k = max(0, math.ceil(0.95 * n) - 1)
        p95 = lats[k]
        err_rate = info["err"] / n
        if err_rate > err_thresh or p95 > p95_ms:
            out.append((_iso(bstart), round(err_rate, 4), p95))
    return out
```
