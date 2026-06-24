## 2024-06-25 - Use ReplyKeyboardMarkup for Core Actions
**Learning:** In Telegram bots, relying purely on slash commands or text matching requires high user effort and typing accuracy, creating friction.
**Action:** Use `ReplyKeyboardMarkup` with descriptive emojis and labels (e.g., "📅 Agenda") for core app modules. Ensure these are intercepted using exact regex matching (`filters.Regex("^📅 Agenda$")`) before any catch-all conversation handlers to make the primary bot features immediately discoverable and accessible with a single tap.
