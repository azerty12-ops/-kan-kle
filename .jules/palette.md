## 2024-05-18 - Discoverability in Telegram Bots
**Learning:** Users often don't know what commands are available in a Telegram bot, or find typing out commands (even with autocomplete) tedious.
**Action:** Use `ReplyKeyboardMarkup` with friendly names (e.g., "📅 Agenda") mapped to core command handlers instead of relying purely on slash commands. This significantly reduces typing friction and makes core features instantly discoverable upon `/start`.
