## 2024-07-01 - Missing Telegram Bot Authentication
**Vulnerability:** The Telegram bot lacked authentication, allowing any user who found the bot to interact with it, accessing potentially sensitive features like personal agenda, local files, and Odoo accounting data.
**Learning:** Telegram bots are public by default unless explicitly restricted. A global TypeHandler middleware with `group=-1` is required to intercept and authorize all updates before they reach specific command handlers.
**Prevention:** Always implement fail-secure authentication middleware (e.g., verifying `ALLOWED_USER_ID`) using `ApplicationHandlerStop()` in the `python-telegram-bot` application setup to restrict access to authorized users only.
