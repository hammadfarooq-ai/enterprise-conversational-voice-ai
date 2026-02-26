import re


OPT_OUT_PATTERN = re.compile(
    r"\b(stop|unsubscribe|remove me|do not call|dnc|quit|opt out|don't call)\b",
    re.IGNORECASE,
)


class ComplianceService:
    async def is_opt_out(self, text: str) -> bool:
        return bool(OPT_OUT_PATTERN.search(text))

    async def opening_disclosure(self) -> str:
        return (
            "This call may be recorded for quality and training. "
            "You can ask us to stop calling at any time."
        )
