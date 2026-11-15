"""In-memory sliding window counters. Client addresses only live here, for
the length of the window, never on disk."""

import threading
import time
from collections import OrderedDict, deque


class RateLimiter:
    def __init__(self, limit: int, window: float, clock=time.time, max_keys: int = 50_000):
        self.limit = limit
        self.window = window
        self.clock = clock
        self.max_keys = max_keys
        self.hits: OrderedDict[str, deque] = OrderedDict()
        self._lock = threading.Lock()

    def _fresh(self, key: str, now: float) -> deque:
        q = self.hits.get(key)
        if q is None:
            q = deque()
            self.hits[key] = q
            while len(self.hits) > self.max_keys:
                self.hits.popitem(last=False)
        else:
            self.hits.move_to_end(key)
        while q and q[0] <= now - self.window:
            q.popleft()
        return q

    def hit(self, key: str) -> bool:
        """Count one request; False when the key is over its limit."""
        with self._lock:
            now = self.clock()
            q = self._fresh(key, now)
            if len(q) >= self.limit:
                return False
            q.append(now)
            return True

    def retry_after(self, key: str) -> int:
        with self._lock:
            q = self.hits.get(key)
            if not q or len(q) < self.limit:
                return 0
            return max(1, int(q[0] + self.window - self.clock()) + 1)
