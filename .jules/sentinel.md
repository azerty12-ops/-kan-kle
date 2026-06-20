## 2024-06-20 - [Missing Telegram Bot Authentication]
**Vulnerability:** The Telegram bot endpoint lacked any form of authentication or authorization, allowing any user who discovered the bot's handle to interact with it.
**Learning:** Because the bot interacts with local system resources (files, calendar, Odoo data) and third-party APIs (Gemini), leaving it unauthenticated exposes sensitive personal data and allows unauthorized API usage.
**Prevention:** Implement a global middleware (e.g., using `TypeHandler` with a negative group number in `python-telegram-bot`) to intercept all updates and verify the user's ID against a configured `ALLOWED_USER_ID` environment variable before processing any commands.
