## 2024-05-24 - Asynchronous I/O in asyncio loop
 **Learning:** The Telegram bot utilizes an `asyncio` event loop. All long-running network or I/O operations (such as calls to the Gemini API) must be executed asynchronously (e.g., using `await model.generate_content_async` with `google.generativeai`) to prevent blocking the application and ensure concurrent user request handling.
 **Action:** Ensure any new I/O bound dependencies or operations use their async variants if available, or are offloaded appropriately.
