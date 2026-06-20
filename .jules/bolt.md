## 2024-06-20 - Non-blocking LLM calls in Asyncio Event Loop
**Learning:** The `python-telegram-bot` uses an asyncio event loop to handle concurrent users. Calling the synchronous `google.generativeai` `generate_content` method inside async handlers completely blocks the main thread for several seconds per request, destroying the bot's ability to handle concurrent messages.
**Action:** Always use the `generate_content_async` equivalent for any network I/O or LLM generation within an asyncio-based application to ensure non-blocking execution.
