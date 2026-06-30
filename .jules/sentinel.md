## 2024-05-24 - Missing Telegram Bot Authentication
**Vulnerability:** The Telegram bot responds to all users who message it, meaning anyone who discovers the bot can access the user's files, agenda, and accounting data.
**Learning:** Public Telegram bots lack built-in authentication restrictions by default; they require explicit middleware or checks to restrict access to the authorized user.
**Prevention:** Always implement a global `TypeHandler` middleware with `group=-1` using `ApplicationHandlerStop()` to block unauthorized users before any command handlers process the update.
