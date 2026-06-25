
## 2025-06-25 - Non-blocking asyncio calls for external services
**Learning:** In an `asyncio` environment like `python-telegram-bot`, making synchronous I/O or network requests (like standard API calls to Gemini) blocks the entire event loop. This causes the bot to become unresponsive to other users or commands while waiting for the API to respond.
**Action:** Always verify if external services offer asynchronous methods (like `generate_content_async` in `google.generativeai`). If so, mark the wrapper methods as `async def` and `await` the external call to yield control back to the event loop during the waiting period.
