## 2024-05-24 - Discoverability of Core Commands
 **Learning:** Users find it tedious to type out commands (e.g., `/agenda`) and may not easily discover available features without an explicit help menu.
 **Action:** Use `ReplyKeyboardMarkup` with persistent buttons (e.g., '📅 Agenda') for core functionalities in the `/start` command response. Map these buttons back to their respective handlers using `MessageHandler(filters.Regex(...), handler)` to reduce typing friction and improve feature discoverability.
