## 2024-05-18 - [Missing Global Authentication in Telegram Bot]
**Vulnerability:** The Telegram bot lacked authentication middleware, exposing sensitive features (file system, agenda, expenses) to any Telegram user.
**Learning:** Telegram bots are inherently public unless restricted. Hardcoded user ID checks or middlewares are necessary to secure personal assistant bots.
**Prevention:** Implement an early-executing global middleware (`group=-1` in python-telegram-bot) to intercept updates and validate user identity against a trusted list or environment variable before any other handlers execute.
