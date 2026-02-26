import asyncio
import socket
import struct
import time

from .codecs import linear16_to_pcmu


class RTPSender:
    def __init__(self, remote_host: str, remote_port: int, payload_type: int = 0):
        self.remote = (remote_host, remote_port)
        self.payload_type = payload_type
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.seq = 0
        self.timestamp = int(time.time() * 8000) & 0xFFFFFFFF
        self.ssrc = 12345678

    def _build_packet(self, payload: bytes) -> bytes:
        vpxcc = 0x80
        mpt = self.payload_type & 0x7F
        header = struct.pack("!BBHII", vpxcc, mpt, self.seq, self.timestamp, self.ssrc)
        self.seq = (self.seq + 1) & 0xFFFF
        self.timestamp = (self.timestamp + 160) & 0xFFFFFFFF
        return header + payload

    async def stream_linear16(self, q: asyncio.Queue):
        while True:
            linear_pcm = await q.get()
            ulaw = linear16_to_pcmu(linear_pcm)
            packet = self._build_packet(ulaw)
            self.sock.sendto(packet, self.remote)
