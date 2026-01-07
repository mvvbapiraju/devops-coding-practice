
def validate_ports(existing, requests):
    out = []
    for p, svc in requests:
        if p < 1024:
            out.append((p, svc, "root-only"))
        elif p > 65535:
            out.append((p, svc, "invalid"))
        elif p in existing and existing[p] != svc:
            out.append((p, svc, "conflict"))
    return out
