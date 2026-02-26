import logging
import time


class SpanTimer:
    def __init__(self, name: str):
        self.name = name
        self.start = time.perf_counter()

    def done(self):
        elapsed_ms = (time.perf_counter() - self.start) * 1000
        logging.getLogger("telemetry").info("span=%s elapsed_ms=%.2f", self.name, elapsed_ms)
