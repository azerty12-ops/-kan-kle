## 2024-11-20 - Non-blocking IO in Telegram Handlers
**Learning:** Using synchronous external API calls (like `generate_content` in `google.generativeai`) inside `python-telegram-bot`'s async handlers (`async def`) blocks the entire asyncio event loop. This prevents the bot from handling concurrent user requests while waiting for the API response.
**Action:** Always use the async equivalent of network/IO methods (e.g., `generate_content_async` over `generate_content`) and `await` them inside async handlers to ensure the event loop remains unblocked and performance scales.
