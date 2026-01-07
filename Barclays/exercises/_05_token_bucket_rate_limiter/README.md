# 05) Token Bucket Rate Limiter

## Question Context
Low-latency guard: per-user and global token buckets to cap QPS with burst.

## Sample Inputs
```python
rl = RateLimiter(user_rate=5, user_burst=10, global_rate=20, global_burst=40)
```

## Expected Outputs
```python
# First ~10 calls allowed; then refills apply.
```

## Solution Approach
Token bucket per user plus a global bucket.

## Complexity (why & how)
O(1) per call; memory O(active users).

## Code
```python
class _Bucket:
    def __init__(self, rate, burst):
        self.rate = float(rate)
        self.burst = float(burst)
        self.tokens = float(burst)
        self.last = None

    def allow(self, now):
        if self.last is None:
            self.last = now
        elapsed = max(0.0, now - self.last)
        self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
        self.last = now
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False

class RateLimiter:
    def __init__(self, user_rate=5, user_burst=10, global_rate=100, global_burst=200):
        self.user_rate, self.user_burst = user_rate, user_burst
        self.global_bucket = _Bucket(global_rate, global_burst)
        self.users = {}

    def allow(self, user_id, now):
        if not self.global_bucket.allow(now):
            return False
        b = self.users.get(user_id)
        if b is None:
            b = self.users[user_id] = _Bucket(self.user_rate, self.user_burst)
        return b.allow(now)
```
