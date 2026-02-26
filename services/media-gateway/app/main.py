import asyncio
import logging

from fastapi import FastAPI

from .config import settings
from .logging_setup import configure_logging
from .rtp_receiver import start_rtp_receiver
from .ws_bridge import WSBridge

configure_logging(settings.log_level)
log = logging.getLogger("media_gateway.main")

app = FastAPI(title="Media Gateway")

rtp_queue: asyncio.Queue = asyncio.Queue(maxsize=1000)
rtp_transport = None
bridge_task: asyncio.Task | None = None


@app.on_event("startup")
async def startup_event():
    global rtp_transport
    rtp_transport = await start_rtp_receiver(settings.media_rtp_host, settings.media_rtp_port, rtp_queue)
    log.info("Media gateway startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    global bridge_task
    if bridge_task:
        bridge_task.cancel()
    if rtp_transport:
        rtp_transport.close()


@app.get("/health")
async def health():
    return {"ok": True, "service": "media-gateway"}


@app.post("/calls/{call_id}/bridge/start")
async def start_bridge(call_id: str, asterisk_rtp_host: str | None = None, asterisk_rtp_port: int | None = None):
    global bridge_task
    if bridge_task and not bridge_task.done():
        return {"ok": False, "message": "bridge already running"}
    bridge = WSBridge(settings.media_orch_ws_url)
    bridge_task = asyncio.create_task(
        bridge.run_call_bridge(call_id, rtp_queue, asterisk_rtp_host, asterisk_rtp_port)
    )
    return {"ok": True, "call_id": call_id}
