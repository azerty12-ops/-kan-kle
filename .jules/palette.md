## 2024-05-24 - Improve Discoverability with ReplyKeyboardMarkup
**Learning:** Telegram bots can suffer from discoverability issues when users have to memorize and type commands manually (e.g. `/agenda`). Typing friction is a barrier to using features.
**Action:** Use `ReplyKeyboardMarkup` attached to the `/start` command response to present core commands as tappable buttons. Route the exact text from these buttons using `MessageHandler` with `filters.Regex` to the respective command functions.
