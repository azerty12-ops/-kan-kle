import logging
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, TypeHandler, ApplicationHandlerStop
from src.services.gemini_service import gemini
from src.services.file_manager import file_manager
from src.services.calendar_service import calendar
from src.services.odoo_service import odoo
from src.services.job_service import job_service

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

ALLOWED_USER_ID = os.getenv("ALLOWED_USER_ID")

async def auth_middleware(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Authentication middleware to block unauthorized users."""
    if not update.effective_user:
        return

    user_id = str(update.effective_user.id)
    if not ALLOWED_USER_ID or user_id != ALLOWED_USER_ID:
        logger.warning(f"Unauthorized access attempt by user {user_id}")
        raise ApplicationHandlerStop()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f"Bonjour {user.first_name} ! Je suis votre assistant personnel.\n\n"
        "Je peux vous aider avec vos tâches quotidiennes.\n"
        "Comment puis-je vous aider aujourd'hui ?"
    )

    keyboard = [
        ['📅 Agenda', '📁 Fichiers'],
        ['💶 Compta', '💼 Emplois']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "Voici les commandes disponibles :\n"
        "/start - Démarrer le bot\n"
        "/help - Afficher cette aide\n"
        "/agenda - Gérer votre agenda\n"
        "/fichiers - Gérer vos fichiers\n"
        "/compta - Gérer votre comptabilité\n"
        "/emplois - Recherche d'emploi\n"
    )
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle normal messages."""
    text = update.message.text

    await update.message.chat.send_action("typing")

    try:
        intent = await gemini.analyze_intent_async(text)

        if intent == "AGENDA":
            prompt = f"L'utilisateur veut gérer son agenda avec cette demande : '{text}'. S'il veut voir ses événements, réponds EXACTEMENT: GET_AGENDA. S'il veut ajouter un événement, extrais le Titre et la Date et réponds EXACTEMENT sous ce format: ADD_EVENT | Titre | Date. Par défaut, si tu n'es pas sûr, réponds GET_AGENDA."
            action = await gemini.generate_response_async(prompt)

            if action.startswith("ADD_EVENT"):
                parts = action.split('|')
                if len(parts) >= 3:
                    result = calendar.add_event(parts[1].strip(), parts[2].strip())
                    await update.message.reply_text(result)
                else:
                    await update.message.reply_text("Désolé, je n'ai pas pu extraire la date correctement.")
            else:
                result = calendar.get_upcoming_events()
                await update.message.reply_text(result)

        elif intent == "COMPTA":
            prompt = f"L'utilisateur veut gérer sa compta avec cette demande : '{text}'. S'il veut voir ses dépenses, réponds EXACTEMENT: GET_COMPTA. S'il veut ajouter une dépense, extrais le Motif et le Montant et réponds EXACTEMENT sous ce format: ADD_EXPENSE | Motif | Montant. Par défaut, si tu n'es pas sûr, réponds GET_COMPTA."
            action = await gemini.generate_response_async(prompt)

            if action.startswith("ADD_EXPENSE"):
                parts = action.split('|')
                if len(parts) >= 3:
                    result = odoo.add_expense(parts[1].strip(), parts[2].strip())
                    await update.message.reply_text(result)
                else:
                    await update.message.reply_text("Je n'ai pas pu comprendre le montant ou le motif. Veuillez réessayer.")
            else:
                result = odoo.get_recent_invoices()
                await update.message.reply_text(result)

        elif intent == "EMPLOI":
            prompt = f"L'utilisateur parle d'emploi : '{text}'. S'il demande de rédiger une lettre de motivation, réponds EXACTEMENT: COVER_LETTER. Sinon, extrait les mots-clés de sa recherche d'emploi et réponds EXACTEMENT sous ce format: SEARCH_JOB | Mots-clés. Par défaut, si tu n'es pas sûr, réponds SEARCH_JOB | général."
            action = await gemini.generate_response_async(prompt)

            if action.startswith("COVER_LETTER"):
                await update.message.reply_text("Je rédige votre lettre de motivation...")
                response = await gemini.generate_cover_letter_async(text, "Profil Polyvalent et Motivé")
                await update.message.reply_text(response)
            else:
                parts = action.split('|')
                keyword = parts[1].strip() if len(parts) >= 2 else "général"
                await update.message.reply_text(f"Je cherche des offres pour '{keyword}' sur Jobs.lu...")
                result = job_service.search_jobs(keyword=keyword)
                await update.message.reply_text(result)

        elif intent == "FICHIERS":
            await fichiers_command(update, context)

        else:
            # CHAT or unknown
            response = await gemini.generate_response_async(text)
            await update.message.reply_text(response)

    except Exception as e:
        await update.message.reply_text(f"Oups, une erreur est survenue: {e}")


async def fichiers_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    source = file_manager.source_folder
    await update.message.reply_text(f"Je vérifie le dossier : {source} ...")
    try:
        result = file_manager.organize_files()
        if "0 fichiers déplacés" in result:
            result += f"\n\nNote : Il n'y a aucun fichier dans le dossier {source} ou bien ce dossier n'existe pas sur votre ordinateur. Vérifiez la configuration de FOLDER_TO_ORGANIZE dans le fichier .env."
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"Erreur lors du rangement: {e}")


async def agenda_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Je vérifie votre agenda...")
    try:
        result = calendar.get_upcoming_events()
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"Erreur avec l'agenda: {e}")


async def compta_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Je me connecte à Odoo pour récupérer vos factures...")
    try:
        result = odoo.get_recent_invoices()
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"Erreur avec la compta: {e}")


async def emplois_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # If user provided a keyword like "/emplois comptable"
    keyword = "comptable"
    if context.args:
        keyword = " ".join(context.args)

    await update.message.reply_text(f"Je cherche des offres pour '{keyword}' sur Jobs.lu...")
    try:
        result = job_service.search_jobs(keyword=keyword)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"Erreur avec la recherche d'emploi: {e}")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    if not TOKEN or TOKEN == "votre_token_telegram_ici":
        logger.error("Veuillez configurer TELEGRAM_BOT_TOKEN dans le fichier .env")
        return

    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Placeholder commands for the modules

    application.add_handler(TypeHandler(Update, auth_middleware), group=-1)

    application.add_handler(CommandHandler("agenda", agenda_command))
    application.add_handler(CommandHandler("fichiers", fichiers_command))

    application.add_handler(CommandHandler("compta", compta_command))
    application.add_handler(CommandHandler("emplois", emplois_command))

    # Exact keyboard matching
    application.add_handler(MessageHandler(filters.Regex('^📅 Agenda$'), agenda_command))
    application.add_handler(MessageHandler(filters.Regex('^📁 Fichiers$'), fichiers_command))
    application.add_handler(MessageHandler(filters.Regex('^💶 Compta$'), compta_command))
    application.add_handler(MessageHandler(filters.Regex('^💼 Emplois$'), emplois_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    logger.info("Démarrage du bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
