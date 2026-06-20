## 2024-06-20 - Telegram Bot Discovery & Interaction
**Learning:** Telegram bots heavily benefit from `ReplyKeyboardMarkup` for core commands. Typing slash commands on mobile is a high friction action. Presenting the main actions directly as large, accessible buttons below the chat input significantly improves discoverability and usability.
**Action:** Always provide custom keyboards for the most frequently used commands in Telegram bots, and ensure they are routed correctly using exact string matches (`Regex` filters) in message handlers to function seamlessly.
