## 2024-05-19 - Asynchronous execution for long I/O tasks
 **Learning:** The Telegram bot utilizes an asyncio event loop. All long-running network or I/O operations (such as calls to the Gemini API) must be executed asynchronously to prevent blocking the application.
 **Action:** Use async versions of the Google GenAI client methods (`await client.aio.models.generate_content`) and implement async wrapper functions (`generate_response_async`, `analyze_intent_async`) in the AI service.
