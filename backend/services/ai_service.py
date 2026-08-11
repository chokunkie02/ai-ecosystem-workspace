import asyncio
import time

class AIService:
    def __init__(self):
        self.model_name = "Qwen-3B-Local"

    async def generate_response(self, prompt: str, max_tokens: int, temperature: float):
        start_time = time.time()
        # Mocking processing
        await asyncio.sleep(1)
        generated_text = f"Response to: {prompt} (Rule-based & {self.model_name})"
        execution_time_ms = (time.time() - start_time) * 1000
        tokens_used = len(prompt.split()) + len(generated_text.split())
        return {
            "generated_text": generated_text,
            "execution_time_ms": execution_time_ms,
            "tokens_used": tokens_used,
            "model_name": self.model_name
        }
    
    async def stream_response(self, prompt: str):
        # Mocking SSE streaming
        words = f"Response to {prompt} from {self.model_name}".split()
        for word in words:
            yield f"data: {word}\n\n"
            await asyncio.sleep(0.2)
        yield "data: [DONE]\n\n"
