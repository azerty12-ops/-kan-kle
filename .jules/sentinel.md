## 2024-06-23 - Missing authentication
**Vulnerability:** The bot currently responds to any user who interacts with it.
**Learning:** Telegram bots need explicit authorization to limit access.
**Prevention:** Always implement a middleware or global handler to check user ID against an ALLOWED_USER_ID.
