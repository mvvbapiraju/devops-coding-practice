
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
