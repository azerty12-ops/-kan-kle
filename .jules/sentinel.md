## 2024-06-24 - Missing Telegram Bot Authorization
**Vulnerability:** The Telegram bot accepted commands and executed requests for ANY user ID, potentially exposing sensitive files, calendar data, and Odoo accounting details.
**Learning:** By default, `python-telegram-bot` processes updates for anyone who finds the bot username. Applications intended for personal or internal use must explicitly filter requests by user ID.
**Prevention:** Implement a global `TypeHandler(Update, auth_middleware, group=-1)` that checks `update.effective_user.id` against an allowed list/environment variable, raising `ApplicationHandlerStop()` for unauthorized users before they hit command handlers.
