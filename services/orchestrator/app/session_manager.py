import asyncio
import json
from typing import Any

from redis.asyncio import Redis


class SessionManager:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self._lock_map: dict[str, asyncio.Lock] = {}

    def _lock_for(self, call_id: str) -> asyncio.Lock:
        if call_id not in self._lock_map:
            self._lock_map[call_id] = asyncio.Lock()
        return self._lock_map[call_id]

    async def init_call(self, call_id: str, seed_data: dict[str, Any]) -> None:
        key = f"call:{call_id}:meta"
        await self.redis.set(key, json.dumps(seed_data), ex=86400)
        await self.redis.delete(f"call:{call_id}:turns")

    async def append_turn(self, call_id: str, speaker: str, text: str) -> None:
        async with self._lock_for(call_id):
            key = f"call:{call_id}:turns"
            turn = json.dumps({"speaker": speaker, "text": text})
            await self.redis.rpush(key, turn)
            await self.redis.expire(key, 86400)
            await self.redis.ltrim(key, -12, -1)

    async def build_messages(self, call_id: str, user_text: str) -> list[dict[str, str]]:
        raw = await self.redis.lrange(f"call:{call_id}:turns", 0, -1)
        messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    "You are a compliant US outbound sales assistant. Keep responses concise and polite. "
                    "Respect opt-out requests immediately."
                ),
            }
        ]
        for item in raw:
            turn = json.loads(item)
            role = "assistant" if turn["speaker"] == "assistant" else "user"
            messages.append({"role": role, "content": turn["text"]})
        messages.append({"role": "user", "content": user_text})
        return messages

    async def set_dnc(self, call_id: str) -> None:
        await self.redis.set(f"call:{call_id}:dnc", "1", ex=2592000)
