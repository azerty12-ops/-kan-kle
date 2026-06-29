## 2024-06-29 - Telegram Bot Command Discoverability
**Learning:** Text-based chat interfaces hide core functionality unless users memorize slash commands, increasing friction. The existing `/start` menu only listed text instructions.
**Action:** Always implement `ReplyKeyboardMarkup` with `resize_keyboard=True` (for mobile viewports) for top-level commands to provide persistent visual buttons, drastically improving discoverability and reducing typing effort.
