from openai import AsyncOpenAI


class LLMEngine:
    def __init__(self, api_key: str, model: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def stream_reply(self, messages: list[dict[str, str]], on_delta) -> None:
        stream = await self.client.responses.create(
            model=self.model,
            input=messages,
            stream=True,
            temperature=0.4,
        )
        async for event in stream:
            if event.type == "response.output_text.delta":
                await on_delta(event.delta)
