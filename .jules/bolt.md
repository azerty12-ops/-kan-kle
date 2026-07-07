## 2024-05-18 - [Avoid Blocking Asyncio with Synchronous LLM Calls]
**Learning:** The telegram bot runs on Python's asyncio event loop. Using synchronous AI calls (`model.generate_content`) in standard async handlers completely blocks the main thread, freezing the bot for all other interactions while waiting for the LLM.
**Action:** Always use the async variants of generative AI SDKs (e.g., `await model.generate_content_async`) in any service class method that might be called from an async bot handler.
