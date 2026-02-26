import logging

import httpx
from fastapi import FastAPI

from .asterisk_ari_client import AsteriskARIClient
from .config import settings
from .logging_setup import configure_logging
from .schemas import StartOutboundCallRequest, EndOutboundCallRequest
from .vicidial_client import VicidialClient

configure_logging(settings.log_level)
log = logging.getLogger("dialer_control.main")

app = FastAPI(title="Dialer Control Service")
vicidial = VicidialClient(settings.vicidial_api_url, settings.vicidial_user, settings.vicidial_pass)
ari = AsteriskARIClient(settings.asterisk_ari_url, settings.asterisk_ari_user, settings.asterisk_ari_pass)


@app.get("/health")
async def health():
    return {"ok": True, "service": "dialer-control"}


@app.post("/calls/start")
async def start_call(req: StartOutboundCallRequest):
    async with httpx.AsyncClient(timeout=15) as client:
        await client.post(
            f"{settings.orchestrator_url}/calls/start",
            json={
                "call_id": req.call_id,
                "lead_phone": req.lead_phone,
                "campaign_name": req.campaign_name,
                "metadata": req.metadata,
            },
        )
        await client.post(f"{settings.media_gateway_url}/calls/{req.call_id}/bridge/start")

    # Hook for real ARI originate:
    # await ari.originate(endpoint=f"SIP/{req.lead_phone}@carrier-trunk", app="voice-ai", app_args=req.call_id)

    return {"ok": True, "call_id": req.call_id}


@app.post("/calls/end")
async def end_call(req: EndOutboundCallRequest):
    async with httpx.AsyncClient(timeout=15) as client:
        await client.post(
            f"{settings.orchestrator_url}/calls/end",
            json={"call_id": req.call_id, "disposition": req.disposition},
        )
    await vicidial.mark_disposition(req.call_id, req.disposition)
    return {"ok": True, "call_id": req.call_id, "disposition": req.disposition}
