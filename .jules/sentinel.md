# Sentinel Journal

## 2024-06-18 - [Missing Authorization]
**Vulnerability:** The Telegram bot did not restrict interactions to the authorized owner. Anyone could message the bot, potentially exposing local data (agenda, compta) or consuming API quotas (Gemini).
**Learning:** Telegram bots are accessible to anyone by default unless explicit filtering is applied.
**Prevention:** Always implement a global authorization check (e.g., using `TypeHandler` with `ApplicationHandlerStop` in python-telegram-bot) based on a configured allowed user ID.
