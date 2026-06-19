## 2024-06-20 - Asynchronous API calls in python-telegram-bot
**Learning:** In python-telegram-bot architectures using `asyncio`, making synchronous network calls (like `model.generate_content` from Gemini API) blocks the entire event loop, preventing concurrent handling of other user messages.
**Action:** Always use the asynchronous versions of I/O bound libraries (e.g., `await model.generate_content_async`) within `async def` handlers to enable concurrency and improve throughput.
