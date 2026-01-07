
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
