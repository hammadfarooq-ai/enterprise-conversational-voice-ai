from pydantic import BaseModel, Field


class StartOutboundCallRequest(BaseModel):
    call_id: str = Field(..., min_length=1)
    lead_phone: str = Field(..., min_length=7)
    campaign_name: str = Field(..., min_length=1)
    metadata: dict = Field(default_factory=dict)


class EndOutboundCallRequest(BaseModel):
    call_id: str
    disposition: str = "completed"
