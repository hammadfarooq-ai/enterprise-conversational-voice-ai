import asyncio
import logging

import websockets

from .codecs import pcmu_to_linear16

log = logging.getLogger("ws_bridge")


class WSBridge:
    def __init__(self, orchestrator_base_url: str):
        self.orchestrator_base_url = orchestrator_base_url.rstrip("/")

    async def run_call_bridge(self, call_id: str, rtp_packet_q: asyncio.Queue) -> None:
        ws_url = f"{self.orchestrator_base_url}/{call_id}"
        async with websockets.connect(ws_url, max_size=None, ping_interval=15) as ws:
            log.info("Connected to orchestrator ws for call_id=%s", call_id)

            async def send_audio():
                while True:
                    pkt = await rtp_packet_q.get()
                    pcm = pcmu_to_linear16(pkt.payload)
                    await ws.send(pcm)

            async def recv_audio():
                while True:
                    _ = await ws.recv()
                    # Hook point: send synthesized audio back to Asterisk via RTP sender.

            sender = asyncio.create_task(send_audio())
            receiver = asyncio.create_task(recv_audio())
            done, pending = await asyncio.wait([sender, receiver], return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
            for task in done:
                if task.exception():
                    raise task.exception()
