
def deep_merge(a, b, protected=set(), path=()):
    out = {} if a is None else dict(a)
    violations = []
    for k, v in (b or {}).items():
        p = path + (k,)
        if p in protected:
            violations.append(p)
            continue
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k], vs = deep_merge(out[k], v, protected, p)
            violations.extend(vs)
        else:
            out[k] = v
    return out, violations

def merge_config(base, env, runtime, protected):
    x, v1 = deep_merge(base, env, protected)
    y, v2 = deep_merge(x, runtime, protected)
    return y, (v1 + v2)
