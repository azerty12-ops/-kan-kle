## 2025-02-18 - Optimize asynchronous long-running tasks
 **Learning:** The Telegram bot runs an `asyncio` event loop. Synchronous calls to external APIs like Gemini blocked the entire event loop, preventing the bot from responding to other incoming updates or performing other tasks concurrently.
 **Action:** We replaced the deprecated `google-generativeai` package with `google-genai` and refactored `GeminiService` methods to use `client.aio.models.generate_content` and be fully `async`. We now `await` these calls in `src/bot/main.py`.
