
def _as_list(x):
    return x if isinstance(x, list) else [x]

def kms_find_wildcards(policy, allowed=set()):
    bad = []
    for st in policy.get("Statement", []):
        acts = set(_as_list(st.get("Action", [])))
        res  = set(_as_list(st.get("Resource", [])))
        pr   = set(_as_list(st.get("Principal", [])))
        if "kms:*" in acts and "*" in res and not pr <= allowed:
            bad.append(st)
    return bad
