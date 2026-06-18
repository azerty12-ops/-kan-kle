## 2024-06-18 - Appels asynchrones avec Gemini
 **Learning:** Les appels synchrones aux API externes comme Gemini dans le handler de messages bloquent l'event loop d'asyncio du bot Telegram, causant des lenteurs ou des blocages lors de multiples requêtes.
 **Action:** Utiliser les méthodes asynchrones (ex: `generate_content_async`) fournies par la librairie `google.generativeai` pour les opérations I/O intensives afin de maintenir la réactivité de l'application.
