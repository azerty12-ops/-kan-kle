## 2024-05-24 - Async Gemini API Calls
**Learning:** Synchronous API calls in `python-telegram-bot` block the entire asyncio event loop, preventing concurrent message handling for other users.
**Action:** Always use async methods (like `generate_content_async`) for external API calls within the bot handlers to ensure non-blocking performance.
