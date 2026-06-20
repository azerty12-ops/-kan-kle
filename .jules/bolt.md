## 2024-05-20 - [Asynchronous API calls]
 **Learning:** The Telegram bot utilizes an asyncio event loop. Blocking API calls halt the loop.
 **Action:** All long-running network or I/O operations must be executed asynchronously (e.g., using await model.generate_content_async with google.generativeai) to prevent blocking the application and ensure concurrent user request handling.
