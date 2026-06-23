## 2024-05-24 - Async IO blocking in python-telegram-bot
**Learning:** Making synchronous network calls (like `model.generate_content`) inside `python-telegram-bot`'s async handlers blocks the main `asyncio` event loop. This leads to the bot freezing and not being able to process other user messages concurrently.
**Action:** Always use the async variants of I/O bound libraries when integrating with an async framework. For the `google.generativeai` SDK, switch to `await model.generate_content_async` inside an `async def` function to yield control back to the event loop during the network wait.
