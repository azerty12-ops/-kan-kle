## 2024-06-16 - [Missing Access Control in Telegram Bot]
**Vulnerability:** Anyone on Telegram can interact with the bot and execute commands to read files, calendar events, and expenses. There is no access control restricting the bot to its owner.
**Learning:** The `python-telegram-bot` application does not include built-in authorization mechanisms. If you don't restrict updates to a specific user, anyone who discovers the bot's handle can access the local environment.
**Prevention:** Implement a global middleware (`TypeHandler` on `Update`) running at `group=-1` to verify `update.effective_user.id` against an `ALLOWED_USER_ID` environment variable and raise `ApplicationHandlerStop` if unauthorized.
