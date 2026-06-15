## 2024-05-24 - Async IO for Network Calls
**Learning:** In the python-telegram-bot framework, making synchronous network calls (like to the Gemini API) inside message handlers blocks the entire `asyncio` event loop. This prevents the bot from handling other concurrent user requests, severely impacting performance and responsiveness.
**Action:** Always use asynchronous clients (e.g., `client.aio.models.generate_content` instead of `client.models.generate_content`) and `await` for any external API or I/O-bound operations within the bot architecture.
