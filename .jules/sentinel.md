## 2024-06-23 - Authorization Bypass via Missing Middleware

**Vulnerability:** The personal assistant Telegram bot lacked access control, allowing any Telegram user to interact with the bot, access local files, and interact with configured services (like Google Calendar, Odoo) simply by finding the bot's username and starting a chat.
**Learning:** In `python-telegram-bot`, global state changes or universal restrictions must be enforced using a `TypeHandler` mapped to all `Update` objects and registered with `group=-1`. This intercepts the event *before* any typical command or message handlers are invoked.
**Prevention:** Always define and register a global authentication middleware (`auth_middleware`) using `ApplicationHandlerStop()` to explicitly halt the processing of events originating from unauthorized user IDs when exposing single-user or administrative bots.
