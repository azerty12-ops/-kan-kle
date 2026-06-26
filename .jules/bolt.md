## 2024-05-24 - Async Gemini API Calls in Telegram Bot
**Learning:** Using synchronous Gemini API calls (`generate_content`) within `python-telegram-bot`'s async handlers blocks the `asyncio` event loop, causing performance bottlenecks and preventing concurrent processing of user requests.
**Action:** Use the non-blocking `generate_content_async` method and make all wrapping service functions `async` to enable concurrent handling of user requests without blocking the event loop.
