## 2024-06-25 - Non-blocking async Telegram API calls
**Learning:** In python-telegram-bot, synchronous blocking calls (like `model.generate_content`) inside message handlers will block the main `asyncio` event loop. This prevents the bot from handling other users concurrent messages or updates, severely degrading multi-user performance.
**Action:** Always use the async equivalent methods (`await model.generate_content_async`) for long-running network or I/O operations inside `async def` Telegram handlers to allow the event loop to yield control.
