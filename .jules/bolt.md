## 2024-05-15 - Unblocking the asyncio event loop
**Learning:** Synchronous calls to the Gemini API (`generate_content`) within `python-telegram-bot`'s `asyncio` handlers block the entire event loop. This causes the bot to process one request at a time, severely degrading performance when multiple users interact concurrently or during slower API responses.
**Action:** Always use the asynchronous versions of network calls (`await model.generate_content_async`) within Telegram handlers to allow the event loop to yield execution and handle concurrent requests efficiently.
