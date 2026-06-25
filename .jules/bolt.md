## 2024-06-25 - Blocking IO in Async Event Loop
**Learning:** Using synchronous network calls (`generate_content`) in an `asyncio` application (like python-telegram-bot) blocks the entire event loop, preventing the bot from processing other users' messages concurrently.
**Action:** Always use the async versions of I/O bound libraries (e.g., `generate_content_async` for google.generativeai) and `await` them in async handlers.
