## 2026-06-26 - [Add Authentication Middleware]
**Vulnerability:** The Telegram bot was accessible to anyone who knew the bot's username or token, allowing unauthorized users to interact with it, add events to the user's agenda, and potentially access private data.
**Learning:** Personal assistant bots need strict authentication. Without an `ALLOWED_USER_ID` check, any Telegram user can trigger command handlers. In `python-telegram-bot`, global middleware via `TypeHandler` with `group=-1` is essential for intercepting all requests before they hit command handlers.
**Prevention:** Always implement an authorization check (e.g., matching `update.effective_user.id` against an allowed list/ID) as global middleware for any bot managing personal or sensitive data.
