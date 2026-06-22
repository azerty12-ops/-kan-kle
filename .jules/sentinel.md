## 2025-02-26 - Missing Authentication in Telegram Bot
**Vulnerability:** The Telegram bot previously processed all incoming updates indiscriminately, allowing any user on Telegram to interact with the bot and execute commands that manipulate local files and view private data (agenda, compta).
**Learning:** Telegram bots are inherently public unless explicitly restricted. Even if the bot is a "personal assistant," anyone who discovers its username can interact with it.
**Prevention:** Always implement an authentication middleware (e.g., using `TypeHandler(Update, restrict_access)` with `group=-1`) that verifies `update.effective_user.id` against an explicitly allowed `ALLOWED_USER_ID` before processing any further handlers. Halt unauthenticated updates using `ApplicationHandlerStop()`.
