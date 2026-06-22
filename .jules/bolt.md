## 2024-06-25 - Use async methods for external API calls
**Learning:** Synchronous network calls (like `gemini.generate_content`) block the entire `asyncio` event loop in python-telegram-bot, causing performance bottlenecks and preventing concurrent user handling.
**Action:** Always use the async variants of API calls (e.g., `generate_content_async`) inside `async def` handlers to ensure the bot remains responsive under load.
