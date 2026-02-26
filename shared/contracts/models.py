from dataclasses import dataclass


@dataclass
class CallRecord:
    call_id: str
    lead_phone: str
    campaign_name: str
    disposition: str = "in_progress"
