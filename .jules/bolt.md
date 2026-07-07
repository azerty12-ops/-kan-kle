## 2024-05-19 - [Blocking I/O in Asyncio Event Loop]
**Learning:** The telegram bot uses `asyncio`, but network calls to Gemini (e.g., `gemini.generate_response`) are currently using synchronous methods and blocking the event loop.
**Action:** When using Gemini in this bot, use the `async` version of the API (`generate_content_async` instead of `generate_content`) and `await` it to prevent blocking the single thread and allow concurrent handling of Telegram updates.
