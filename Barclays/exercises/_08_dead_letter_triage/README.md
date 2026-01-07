# 08) Dead Letter Triage

## Question Context
Route valid events by topic and capture rejects with reasons to watch DLQ spikes.

## Sample Inputs
```python
msgs=['{"domain":"auth","type":"userGranted","id":1}',"not-json"]
```

## Expected Outputs
```python
({"auth.userGranted":[{"domain":"auth","type":"userGranted","id":1}]},[("not-json","Expecting value: line 1 column 1 (char 0)")])
```

## Solution Approach
Try/except parse, schema-check required keys, route valid messages, log rejects.

## Complexity (why & how)
O(n) time; memory depends on retained batch size.

## Code
```python
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
```
