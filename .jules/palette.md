## 2024-10-25 - Discoverability via ReplyKeyboardMarkup
**Learning:** Telegram bot commands (`/command`) require typing which increases friction for core actions. Users benefit from persistent visible buttons for main interactions.
**Action:** Use `ReplyKeyboardMarkup` for core navigation commands and map the button text using `MessageHandler` with `filters.Regex` exact string matching before the catch-all text handler.
