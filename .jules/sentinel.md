## 2024-05-18 - [Fix Unauthorized Access to Bot]
 **Vulnerability:** [The bot processed messages and commands from any Telegram user, exposing personal files, agenda, and accounting data.]
 **Learning:** [Without an authorization check, anyone discovering the bot username can interact with the system and exploit its functionalities.]
 **Prevention:** [Implement a global TypeHandler registered with group=-1 to check the update.effective_user.id against an ALLOWED_USER_ID environment variable, raising ApplicationHandlerStop() for unauthorized users.]