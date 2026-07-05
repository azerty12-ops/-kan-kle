## 2024-05-24 - Async IO for Network Calls
**Learning:** Long-running synchronous network calls (like `model.generate_content` in `google-generativeai`) block the `asyncio` event loop in telegram bots, freezing the application and preventing it from handling concurrent requests.
**Action:** Always use the asynchronous equivalents (e.g., `await model.generate_content_async`) and `async def` methods for external API interactions in `python-telegram-bot` handlers.
