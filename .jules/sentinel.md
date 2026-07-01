## 2024-05-24 - Unauthenticated Access to Telegram Bot
 **Vulnerability:** The Telegram bot previously processed commands and messages from any user interacting with it, lacking authorization checks.
 **Learning:** In `python-telegram-bot`, commands and messages are public by default unless explicitly restricted.
 **Prevention:** Implement a global `TypeHandler(Update, auth_callback)` registered with `group=-1` to intercept all updates. Retrieve the `ALLOWED_USER_ID` from the environment, ensure it is validated carefully (e.g. catch `ValueError`), and raise `ApplicationHandlerStop()` if the `effective_user.id` does not match to block unauthorized access.
