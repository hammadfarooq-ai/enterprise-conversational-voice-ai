import httpx


class VicidialClient:
    def __init__(self, base_url: str, user: str, password: str):
        self.base_url = base_url
        self.user = user
        self.password = password

    async def mark_disposition(self, call_id: str, disposition: str) -> dict:
        if not self.base_url:
            return {"ok": True, "message": "Vicidial endpoint not configured"}
        params = {
            "source": "voice-ai",
            "user": self.user,
            "pass": self.password,
            "function": "update_fields",
            "lead_id": call_id,
            "dispo": disposition,
        }
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            return {"ok": True, "status_code": response.status_code}
