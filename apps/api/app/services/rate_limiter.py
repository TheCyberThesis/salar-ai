from collections import defaultdict, deque
from time import time

from fastapi import HTTPException, Request

from app.config import get_settings


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self.requests: dict[str, deque[float]] = defaultdict(deque)

    def check(self, request: Request) -> None:
        settings = get_settings()
        limit = settings.rate_limit_per_minute
        now = time()
        client = request.client.host if request.client else "unknown"
        queue = self.requests[client]
        while queue and now - queue[0] > 60:
            queue.popleft()
        if len(queue) >= limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again shortly.")
        queue.append(now)


rate_limiter = InMemoryRateLimiter()
