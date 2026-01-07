# 09) Iac Drift Detector

## Question Context
Compare resource snapshots to report creates, deletes, and updates with field-level diffs.

## Sample Inputs
```python
before=[{"id":"sg-1","name":"web","ports":[80]}]; after=[{"id":"sg-1","name":"web","ports":[80,443]}]
```

## Expected Outputs
```python
creates=[]; updates=[("sg-1",{"ports":([80],[80,443])})]; deletes=[]
```

## Solution Approach
Index by ID and compute set differences; shallow per-field diffs for shared IDs.

## Complexity (why & how)
O(n+m) time/space.

## Code
```python
def shallow_diff(a, b):
    keys = set(a) | set(b)
    diff = {}
    for k in keys:
        if a.get(k) != b.get(k):
            diff[k] = (a.get(k), b.get(k))
    return diff

def drift(before, after, key="id"):
    b = {x[key]: x for x in before}
    a = {x[key]: x for x in after}
    creates = [a[k] for k in a.keys() - b.keys()]
    deletes = [b[k] for k in b.keys() - a.keys()]
    updates = []
    for k in a.keys() & b.keys():
        d = shallow_diff(b[k], a[k])
        if d:
            updates.append((k, d))
    return creates, updates, deletes
```
