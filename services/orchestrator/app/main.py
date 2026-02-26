import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from redis.asyncio import from_url as redis_from_url

from .compliance import ComplianceService
from .config import settings
from .deepgram_stream import DeepgramStreamer
from .elevenlabs_stream import ElevenLabsTTS
from .logging_setup import configure_logging
from .openai_stream import LLMEngine
from .pipeline import CallPipeline
from .schemas import CallStartRequest, CallEndRequest
from .session_manager import SessionManager

configure_logging(settings.log_level)
log = logging.getLogger("orchestrator.main")

redis_client = redis_from_url(settings.redis_url, decode_responses=False)
session_manager = SessionManager(redis_client)
compliance_service = ComplianceService()
stt = DeepgramStreamer(settings.deepgram_api_key)
llm = LLMEngine(settings.openai_api_key, settings.openai_model)
tts = ElevenLabsTTS(settings.elevenlabs_api_key, settings.elevenlabs_voice_id)
pipeline = CallPipeline(session_manager, compliance_service, stt, llm, tts)

active_calls: dict[str, dict[str, asyncio.Queue]] = {}
active_tasks: dict[str, asyncio.Task] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_client.aclose()


app = FastAPI(title="Voice AI Orchestrator", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"ok": True, "service": "orchestrator"}


@app.post("/calls/start")
async def call_start(req: CallStartRequest):
    await session_manager.init_call(
        req.call_id,
        {
            "lead_phone": req.lead_phone,
            "campaign_name": req.campaign_name,
            "metadata": req.metadata,
        },
    )
    return {"ok": True, "call_id": req.call_id}


@app.post("/calls/end")
async def call_end(req: CallEndRequest):
    if req.call_id in active_tasks:
        active_tasks[req.call_id].cancel()
        active_tasks.pop(req.call_id, None)
    active_calls.pop(req.call_id, None)
    return {"ok": True, "call_id": req.call_id, "disposition": req.disposition}


@app.websocket("/ws/media/{call_id}")
async def media_websocket(websocket: WebSocket, call_id: str):
    await websocket.accept()
    log.info("Media websocket connected call_id=%s", call_id)

    pcm_in = asyncio.Queue(maxsize=300)
    tts_audio_out = asyncio.Queue(maxsize=300)
    active_calls[call_id] = {"pcm_in": pcm_in, "tts_audio_out": tts_audio_out}

    pipeline_task = asyncio.create_task(pipeline.run(call_id, pcm_in, tts_audio_out))
    active_tasks[call_id] = pipeline_task

    async def recv_loop():
        while True:
            data = await websocket.receive_bytes()
            await pcm_in.put(data)

    async def send_loop():
        while True:
            chunk = await tts_audio_out.get()
            await websocket.send_bytes(chunk)

    recv_task = asyncio.create_task(recv_loop())
    send_task = asyncio.create_task(send_loop())

    try:
        done, pending = await asyncio.wait(
            [recv_task, send_task, pipeline_task], return_when=asyncio.FIRST_COMPLETED
        )
        for task in pending:
            task.cancel()
        for task in done:
            if task.exception():
                raise task.exception()
    except WebSocketDisconnect:
        log.info("Media websocket disconnected call_id=%s", call_id)
    except Exception as exc:
        log.exception("Websocket error call_id=%s: %s", call_id, exc)
        raise HTTPException(status_code=500, detail="Media websocket failure") from exc
    finally:
        active_calls.pop(call_id, None)
        active_tasks.pop(call_id, None)
