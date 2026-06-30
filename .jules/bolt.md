## 2024-05-24 - Avoid Synchronous I/O in Asyncio Event Loops
**Learning:** Using synchronous network calls (like `model.generate_content`) inside a Telegram bot that runs on an `asyncio` event loop blocks the entire loop. This means the bot cannot process concurrent requests while waiting for the Gemini API response.
**Action:** Always use the asynchronous versions of I/O bound functions (e.g., `model.generate_content_async`) and `await` them when integrating external APIs into `asyncio` applications like `python-telegram-bot`.
