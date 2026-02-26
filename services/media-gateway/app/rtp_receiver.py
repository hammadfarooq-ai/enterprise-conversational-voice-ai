import asyncio
import logging
import struct
from dataclasses import dataclass

log = logging.getLogger("rtp_receiver")

RTP_HEADER_FMT = "!BBHII"
RTP_HEADER_SIZE = 12


@dataclass
class RTPPacket:
    payload_type: int
    seq: int
    timestamp: int
    ssrc: int
    payload: bytes


def parse_rtp(data: bytes) -> RTPPacket:
    if len(data) < RTP_HEADER_SIZE:
        raise ValueError("RTP packet too short")
    b1, b2, seq, timestamp, ssrc = struct.unpack(RTP_HEADER_FMT, data[:RTP_HEADER_SIZE])
    version = b1 >> 6
    if version != 2:
        raise ValueError("Unsupported RTP version")
    cc = b1 & 0x0F
    header_len = RTP_HEADER_SIZE + (4 * cc)
    payload_type = b2 & 0x7F
    return RTPPacket(
        payload_type=payload_type,
        seq=seq,
        timestamp=timestamp,
        ssrc=ssrc,
        payload=data[header_len:],
    )


class RTPProtocol(asyncio.DatagramProtocol):
    def __init__(self, packet_queue: asyncio.Queue):
        self.packet_queue = packet_queue

    def datagram_received(self, data: bytes, addr):
        try:
            packet = parse_rtp(data)
            self.packet_queue.put_nowait(packet)
        except Exception as exc:
            log.warning("Bad RTP packet from %s: %s", addr, exc)


async def start_rtp_receiver(host: str, port: int, packet_queue: asyncio.Queue):
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
        lambda: RTPProtocol(packet_queue),
        local_addr=(host, port),
        reuse_port=True,
    )
    log.info("RTP receiver listening on %s:%s", host, port)
    return transport
