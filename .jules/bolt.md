## 2024-06-25 - Blocking IO in Async Event Loop
**Learning:** Found that calls to the Gemini API were implemented synchronously, which is a common anti-pattern in `asyncio` applications like `python-telegram-bot` instances, where blocking the main thread prevents processing other incoming updates concurrently.
**Action:** Always ensure network I/O operations are implemented asynchronously (e.g., using `await model.generate_content_async`) in Telegram bot handlers.
