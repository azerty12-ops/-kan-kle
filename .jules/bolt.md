## 2024-05-24 - Async IO vs Sync IO for External API Calls
**Learning:** Calling synchronous IO functions (like `model.generate_content`) within `async def` handlers in Python-telegram-bot blocks the asyncio event loop. This blocks the main thread and prevents handling any other concurrent requests.
**Action:** Always use the async variants of external API calls (e.g. `await model.generate_content_async`) in any asynchronous bot frameworks to maintain high concurrency.
