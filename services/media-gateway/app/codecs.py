import audioop


def pcmu_to_linear16(payload: bytes) -> bytes:
    return audioop.ulaw2lin(payload, 2)


def linear16_to_pcmu(payload: bytes) -> bytes:
    return audioop.lin2ulaw(payload, 2)
