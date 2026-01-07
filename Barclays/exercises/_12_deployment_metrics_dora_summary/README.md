# 12) Deployment Metrics Dora Summary

## Question Context
Aggregate weekly DORA metrics (fail rate, lead time, MTTR) keyed by ISO week.

## Sample Inputs
```python
deploys=[{"start_ts":"2026-01-06T10:00:00Z","end_ts":"2026-01-06T10:05:00Z","status":"ok","lead_time_min":35,"mttr_min":0}]
```

## Expected Outputs
```python
{"2026-W02":{"change_fail_rate":0.0,"avg_lead_time":35,"avg_mttr":0}}
```

## Solution Approach
Group by ISO week and compute ratios/means.

## Complexity (why & how)
O(n) time; O(#weeks) memory.

## Code
```python
from statistics import mean
from datetime import datetime, timezone

def _to_epoch(ts):
    if isinstance(ts, (int, float)): return int(ts)
    if isinstance(ts, str):
        s = ts.replace('Z', '+00:00')
        return int(datetime.fromisoformat(s).timestamp())
    raise ValueError("Unsupported ts")

def _iso_week_key(ts):
    ep = _to_epoch(ts)
    dt = datetime.fromtimestamp(ep, tz=timezone.utc)
    y, w, _ = dt.isocalendar()
    return f"{y}-W{w:02d}"

def dora_summary(deploys):
    by_week = {}
    for d in deploys:
        wk = _iso_week_key(d["start_ts"])
        by_week.setdefault(wk, []).append(d)
    out = {}
    for wk, arr in by_week.items():
        n = len(arr) or 1
        fails = sum(1 for x in arr if x.get("status") == "fail")
        lead = [x["lead_time_min"] for x in arr if "lead_time_min" in x]
        mttr = [x["mttr_min"] for x in arr if "mttr_min" in x]
        out[wk] = {
            "change_fail_rate": fails / n,
            "avg_lead_time": mean(lead) if lead else 0,
            "avg_mttr": mean(mttr) if mttr else 0
        }
    return out
```
