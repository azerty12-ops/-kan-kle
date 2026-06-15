## 2025-02-18 - Improve discoverability and reduce typing friction
 **Learning:** Telegram bots can have custom keyboards directly attached to messages that persist, making common commands much easier to discover and trigger without typing them.
 **Action:** We implemented a `ReplyKeyboardMarkup` containing `/agenda`, `/fichiers`, `/compta`, and `/emplois` that is sent to the user upon the `/start` command. This ensures the user sees these options immediately and can tap them.
