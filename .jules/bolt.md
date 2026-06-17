## 2026-06-17 - Avoid synchronous I/O blocking in Telegram bot
**Learning:** In a python-telegram-bot application, running synchronous network calls (like the previous `model.generate_content` for Gemini API) blocks the entire asyncio event loop. This prevents the bot from handling other users or updates concurrently while waiting for the API response.
**Action:** Always use the async variants of I/O bound libraries (`generate_content_async` instead of `generate_content`) and `await` them when inside the bot's asynchronous message handlers.
