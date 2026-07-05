## 2024-05-24 - Async API Calls in Event Loop
**Learning:** Telegram bots running in `asyncio` loops will become unresponsive if synchronous network/I/O requests (like calls to `model.generate_content`) are used, because they block the main event loop and prevent concurrent message handling.
**Action:** Always use the asynchronous versions of library methods for network requests (e.g., `model.generate_content_async`) and `await` them in bot handlers to ensure the application remains non-blocking and highly concurrent.
