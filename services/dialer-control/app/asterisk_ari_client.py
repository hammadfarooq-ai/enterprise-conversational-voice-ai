import httpx


class AsteriskARIClient:
    def __init__(self, base_url: str, user: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.auth = (user, password)

    async def originate(self, endpoint: str, app: str, app_args: str) -> dict:
        if not self.base_url:
            return {"ok": True, "message": "ARI endpoint not configured"}
        url = f"{self.base_url}/channels"
        params = {"endpoint": endpoint, "app": app, "appArgs": app_args}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, params=params, auth=self.auth)
            response.raise_for_status()
            return {"ok": True, "status_code": response.status_code}
