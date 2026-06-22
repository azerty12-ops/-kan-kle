## 2024-06-22 - [Asyncio Event Loop Blocking]
**Learning:** The telegram bot runs on an asyncio event loop. Using synchronous API calls (like `model.generate_content`) blocks the main thread, meaning the bot cannot process other incoming messages or commands while waiting for the network response.
**Action:** Always use asynchronous equivalents (like `await model.generate_content_async`) for long-running network or I/O operations in this codebase to ensure concurrent user request handling.
