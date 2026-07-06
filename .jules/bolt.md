## 2024-07-06 - Async Generation
**Learning:** Synchronous network calls (like `model.generate_content`) inside a `python-telegram-bot` application block the main asyncio event loop, causing the bot to freeze and become unresponsive to concurrent users.
**Action:** Always use the asynchronous equivalent (`await model.generate_content_async`) and `async def` for I/O bound tasks in bot handlers to ensure non-blocking execution.
