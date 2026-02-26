import asyncio


class IdempotencyGuard:
    def __init__(self):
        self._seen: set[str] = set()
        self._lock = asyncio.Lock()

    async def check_and_set(self, key: str) -> bool:
        async with self._lock:
            if key in self._seen:
                return False
            self._seen.add(key)
            return True
