## 2024-05-18 - ReplyKeyboardMarkup Interaction
**Learning:** Telegram bot users experience high friction typing out full slash commands or specific phrasing, reducing engagement.
**Action:** Use `ReplyKeyboardMarkup` to present interactive buttons for core navigation features, mapping the exact button text via `MessageHandler(filters.Regex(...))` to bypass complex conversational routing.
