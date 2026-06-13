## 2024-05-24 - Asyncio Blockers in Telegram Bots
**Learning:** Making synchronous network calls (like `gemini.generate_response`) inside an asynchronous request handler (`handle_message`) blocks the entire asyncio event loop. This prevents the bot from processing other incoming messages concurrently, severely impacting throughput and responsiveness under load.
**Action:** Always use asynchronous methods (`await gemini.generate_response_async()`) for long-running I/O operations (like API calls) when operating within an `asyncio` context like `python-telegram-bot`.
