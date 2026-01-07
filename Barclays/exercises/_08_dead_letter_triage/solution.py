
import json

def triage_messages(messages, required=("domain","type")):
    routes = {}
    rejects = []
    for raw in messages:
        try:
            m = json.loads(raw)
            if not all(k in m for k in required):
                raise ValueError("missing required fields")
            topic = f"{m['domain']}.{m['type']}"
            routes.setdefault(topic, []).append(m)
        except Exception as e:
            rejects.append((raw, str(e)))
    return routes, rejects
