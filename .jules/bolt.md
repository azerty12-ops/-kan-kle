## 2024-06-25 - Prevent Event Loop Blocking with async Gemini API
**Learning:** Using synchronous `generate_content` for the Gemini API inside an `asyncio` Telegram bot event loop blocks the entire main thread for all users while waiting for the AI response. This is a severe performance bottleneck for concurrency.
**Action:** Always use the asynchronous `generate_content_async` method (`await self.model.generate_content_async(prompt)`) and ensure any functions wrapping it are `async def` and awaited appropriately.
