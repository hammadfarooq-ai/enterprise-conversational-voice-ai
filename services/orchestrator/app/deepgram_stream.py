import asyncio
import logging

from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents

log = logging.getLogger("deepgram_stream")


class DeepgramStreamer:
    def __init__(self, api_key: str):
        self.client = DeepgramClient(api_key)

    async def transcribe_stream(self, pcm_in: asyncio.Queue, transcript_out: asyncio.Queue) -> None:
        conn = self.client.listen.websocket.v("1")
        loop = asyncio.get_running_loop()

        def on_transcript(_, result, **kwargs):
            alt = result.channel.alternatives[0] if result.channel and result.channel.alternatives else None
            if not alt or not alt.transcript:
                return
            loop.create_task(
                transcript_out.put(
                    {"text": alt.transcript, "final": bool(result.is_final)}
                )
            )

        conn.on(LiveTranscriptionEvents.Transcript, on_transcript)
        conn.start(
            LiveOptions(
                model="nova-2",
                language="en-US",
                encoding="linear16",
                sample_rate=8000,
                channels=1,
                interim_results=True,
                punctuate=True,
            )
        )
        try:
            while True:
                frame = await pcm_in.get()
                conn.send(frame)
        except asyncio.CancelledError:
            log.info("Deepgram stream cancelled")
            raise
        finally:
            conn.finish()
