from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CallEvent:
    event_type: str
    call_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    ts: str = field(default_factory=utc_now)
