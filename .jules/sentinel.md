## 2024-07-08 - Authentication Bypass in Telegram Bot
**Vulnerability:** The Telegram bot handles incoming messages from any user without verifying their identity, allowing any Telegram user to interact with the bot, access local files, and trigger services like Odoo and Calendar.
**Learning:** The lack of global authentication allows unauthorized access to sensitive local resources and services. This happened because `python-telegram-bot` doesn't enforce authentication by default.
**Prevention:** Implement a global `TypeHandler` middleware with `group=-1` to verify the `ALLOWED_USER_ID` against `update.effective_user.id`. Fail closed by raising `ApplicationHandlerStop()` if the user is unauthorized or if the environment variable is misconfigured or missing.
