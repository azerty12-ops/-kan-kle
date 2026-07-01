## 2024-05-14 - [Async IO for Gemini API]
**Learning:** Using synchronous `generate_content()` on the Gemini API in `src/services/gemini_service.py` blocks the `python-telegram-bot` asyncio event loop, causing all concurrent user requests to stall while waiting for network I/O.
**Action:** Always use `await model.generate_content_async()` for Gemini network requests inside async handlers, and ensure service methods are declared `async def`.
