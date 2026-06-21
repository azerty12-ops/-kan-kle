## 2026-06-21 - Asynchronous Handlers and Event Loop Blocking
**Learning:** `python-telegram-bot` utilizes an `asyncio` event loop. Calling synchronous I/O operations (like `model.generate_content`) inside `async def` handlers blocks the main thread, stalling concurrent requests.
**Action:** Always use the asynchronous versions of I/O operations (e.g., `model.generate_content_async` with `await`) inside bot handlers to ensure non-blocking execution and maintain optimal performance.
