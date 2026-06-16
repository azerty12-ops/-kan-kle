## 2024-05-19 - Bot Access Restriction
 **Learning:** The Telegram bot requires strict access control so only the authorized owner can interact with it. In python-telegram-bot, global authentication should use a TypeHandler and `raise ApplicationHandlerStop()` to properly halt update processing.
 **Action:** Implement an auth middleware that checks `update.effective_user.id` against an `ALLOWED_USER_ID` environment variable and raises `ApplicationHandlerStop()` for unauthorized users.
