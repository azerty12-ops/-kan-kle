## 2024-06-20 - Asynchronous LLM API calls in Event Loop
**Learning:** Synchronous network calls (like `model.generate_content`) inside `python-telegram-bot`'s async handlers block the entire `asyncio` event loop. This creates a severe concurrency bottleneck where one slow LLM request blocks all other users from interacting with the bot.
**Action:** Always use the asynchronous versions of network/I/O libraries (e.g., `model.generate_content_async` with `google.generativeai`) and `await` them inside async handlers to ensure the bot can serve multiple users concurrently.
