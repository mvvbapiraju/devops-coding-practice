
import re
_SEMVER = re.compile(r'^(\d+)\.(\d+)\.(\d+)')

def parse_semver(v):
    m = _SEMVER.match(v)
    if not m: 
        raise ValueError(f"Bad semver: {v}")
    return tuple(map(int, m.groups()))

def semver_gate(current, candidate, block_major=True, min_minor_increase=0):
    cur = parse_semver(current)
    new = parse_semver(candidate)
    if new == cur:
        return (False, "no change")
    if new < cur:
        return (False, "downgrade not allowed")
    if block_major and new[0] != cur[0]:
        return (False, "major upgrades blocked")
    if new[0] == cur[0] and (new[1] - cur[1]) < min_minor_increase and new <= cur:
        return (False, "insufficient minor increase")
    return (True, "ok")
