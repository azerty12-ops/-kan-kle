## 2024-05-24 - Blocking the Asyncio Event Loop with Synchronous API Calls
 **Learning:** Calling synchronous methods (like `model.generate_content()`) within asynchronous Telegram bot handlers blocks the event loop, preventing the bot from processing other concurrent updates.
 **Action:** Ensure all I/O bound or network operations, such as Gemini API calls, use their asynchronous equivalents (e.g., `await model.generate_content_async()`) and that the corresponding service methods are defined with `async def`.
