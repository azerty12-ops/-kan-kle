## 2024-05-18 - [Missing Access Control]
**Vulnerability:** The Telegram bot lacked global access control, allowing any Telegram user to interact with the bot and potentially access sensitive local data (calendar, files, accounting) if they discovered the bot's username.
**Learning:** Telegram bots do not have built-in restriction mechanisms to their creator; this must be explicitly implemented at the application level.
**Prevention:** Always implement a global middleware checking against an authorized user identifier (like `ALLOWED_USER_ID`) before processing any updates, especially when the bot has access to private or local system resources.
