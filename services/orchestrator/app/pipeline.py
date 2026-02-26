import asyncio
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

from .fallback import fallback_text
from .sentiment import score_sentiment

log = logging.getLogger("pipeline")


class CallPipeline:
    def __init__(self, session_manager, compliance, stt, llm, tts):
        self.session_manager = session_manager
        self.compliance = compliance
        self.stt = stt
        self.llm = llm
        self.tts = tts

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.2, min=0.2, max=2))
    async def _call_llm(self, messages, on_delta):
        await self.llm.stream_reply(messages, on_delta)

    async def run(self, call_id: str, pcm_in: asyncio.Queue, tts_audio_out: asyncio.Queue) -> None:
        transcript_q = asyncio.Queue()
        stt_task = asyncio.create_task(self.stt.transcribe_stream(pcm_in, transcript_q))

        try:
            while True:
                event = await transcript_q.get()
                text = event.get("text", "").strip()
                if not text or not event.get("final"):
                    continue

                if await self.compliance.is_opt_out(text):
                    await self.session_manager.append_turn(call_id, "user", text)
                    await self.session_manager.set_dnc(call_id)
                    end_msg = "Understood. We will not call again. Goodbye."
                    await self.session_manager.append_turn(call_id, "assistant", end_msg)
                    await self.tts.stream_tts(end_msg, tts_audio_out)
                    break

                _ = score_sentiment(text)
                await self.session_manager.append_turn(call_id, "user", text)
                messages = await self.session_manager.build_messages(call_id, text)

                out_tokens: list[str] = []

                async def on_delta(delta: str):
                    out_tokens.append(delta)

                try:
                    await self._call_llm(messages, on_delta)
                    assistant_text = "".join(out_tokens).strip() or "Could you repeat that?"
                except Exception as exc:
                    log.exception("LLM failure for call_id=%s: %s", call_id, exc)
                    assistant_text = await fallback_text()

                await self.session_manager.append_turn(call_id, "assistant", assistant_text)
                await self.tts.stream_tts(assistant_text, tts_audio_out)
        finally:
            stt_task.cancel()
