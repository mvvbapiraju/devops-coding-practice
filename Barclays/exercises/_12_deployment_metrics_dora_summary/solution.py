
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
