## 2024-06-25 - Missing Authentication on Telegram Bot
**Vulnerability:** The Telegram Bot lacked authentication, meaning anyone who found the bot could interact with it, potentially exposing the user's agenda, files, and running commands on their machine.
**Learning:** Telegram bots are inherently public unless explicitly restricted. Even if the bot's username is secret, people can discover it or stumble upon it. We must always validate the `update.effective_user.id`.
**Prevention:** Implement a global middleware (`TypeHandler` with `group=-1`) that checks the user's ID against an `ALLOWED_USER_ID` environment variable and raises `ApplicationHandlerStop()` for unauthorized users.
