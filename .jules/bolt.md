## 2024-06-23 - Async API Calls
**Learning:** Synchronous calls to external APIs block the event loop, causing delays in handling concurrent requests.
**Action:** Refactored Gemini API calls to use the async equivalent `generate_content_async` to prevent blocking the Telegram bot's async loop.
