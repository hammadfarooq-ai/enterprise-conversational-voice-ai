from pydantic import BaseModel, Field


class CallStartRequest(BaseModel):
    call_id: str = Field(..., min_length=1)
    lead_phone: str
    campaign_name: str
    metadata: dict = Field(default_factory=dict)


class CallEndRequest(BaseModel):
    call_id: str
    disposition: str = "completed"
