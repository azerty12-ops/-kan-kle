## 2024-05-24 - Async IO blocking in python-telegram-bot
**Learning:** Synchronous network calls (like `model.generate_content`) inside `python-telegram-bot` handlers block the `asyncio` event loop. This causes the bot to become unresponsive to other users and updates while waiting for the API to respond, creating a massive bottleneck for concurrent usage.
**Action:** Always use the `_async` versions of I/O bound library methods (e.g. `await model.generate_content_async`) and declare the corresponding wrapper services as `async def` so they can be properly awaited inside telegram handlers.
