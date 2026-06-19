## 2024-06-19 - [Async API calls inside asyncio application]
**Learning:** Using synchronous operations (`google.generativeai.GenerativeModel.generate_content`) inside an `asyncio` event loop (such as the one used by `python-telegram-bot`) blocks the main thread. This causes the bot to freeze for all users during the API call, severely impacting concurrency and performance.
**Action:** Always use the async variants of API calls (e.g., `generate_content_async`) when inside `asyncio`-based environments to ensure non-blocking concurrent request handling.
