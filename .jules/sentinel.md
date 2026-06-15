## 2025-02-18 - Basic Authentication via Middleware
 **Learning:** Previously, the bot had no restrictions and anyone who found it could potentially execute commands and access local state/API resources.
 **Action:** We added a global `TypeHandler` middleware in `src/bot/main.py` that intercepts all `Update` objects. It verifies `update.effective_user.id` against an `ALLOWED_USER_ID` environment variable. Unrecognized users receive a silent `Application.StopUpdate()`, effectively locking down the bot to its owner.
