import asyncio
import logging

import websockets

from .codecs import pcmu_to_linear16
from .rtp_sender import RTPSender

log = logging.getLogger("ws_bridge")


class WSBridge:
    def __init__(self, orchestrator_base_url: str):
        self.orchestrator_base_url = orchestrator_base_url.rstrip("/")

    async def run_call_bridge(
        self,
        call_id: str,
        rtp_packet_q: asyncio.Queue,
        asterisk_rtp_host: str | None = None,
        asterisk_rtp_port: int | None = None,
    ) -> None:
        ws_url = f"{self.orchestrator_base_url}/{call_id}"
        out_q = asyncio.Queue(maxsize=300)
        sender = None
        sender_task = None
        if asterisk_rtp_host and asterisk_rtp_port:
            sender = RTPSender(asterisk_rtp_host, asterisk_rtp_port)
            sender_task = asyncio.create_task(sender.stream_linear16(out_q))

        async with websockets.connect(ws_url, max_size=None, ping_interval=15) as ws:
            log.info("Connected to orchestrator ws for call_id=%s", call_id)

            async def send_audio():
                while True:
                    pkt = await rtp_packet_q.get()
                    pcm = pcmu_to_linear16(pkt.payload)
                    await ws.send(pcm)

            async def recv_audio():
                while True:
                    chunk = await ws.recv()
                    if isinstance(chunk, bytes) and sender:
                        await out_q.put(chunk)

            tx_task = asyncio.create_task(send_audio())
            rx_task = asyncio.create_task(recv_audio())
            wait_set = [tx_task, rx_task]
            if sender_task:
                wait_set.append(sender_task)

            done, pending = await asyncio.wait(wait_set, return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
            for task in done:
                if task.exception():
                    raise task.exception()
