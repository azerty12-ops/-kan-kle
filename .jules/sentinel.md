## 2024-05-24 - [Fail-Closed Telegram Updates]
**Vulnerability:** Updates lacking an `effective_user` (e.g., channel posts) were bypassed by returning early in auth middleware.
**Learning:** `python-telegram-bot`'s `effective_user` can be None for some updates. Returning early instead of raising `ApplicationHandlerStop` creates a fail-open scenario for these edge cases.
**Prevention:** Always fail-closed (raise `ApplicationHandlerStop`) for missing or malformed data in authentication middleware, even if it seems like an irrelevant update type.
