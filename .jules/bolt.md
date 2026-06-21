## 2024-05-24 - Async LLM Calls in asyncio loop
**Learning:** Synchronous network calls to the Gemini API (`.generate_content()`) inside the Telegram bot's `asyncio` event loop block the entire application. While one user's message is being processed by the LLM, the bot cannot receive or respond to any other messages.
**Action:** Always use the async variants of the Gemini API (`await .generate_content_async()`) and ensure custom wrapper methods (like `GeminiService.generate_response`) are defined as `async def` and properly awaited in the bot handlers.
