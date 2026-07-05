import logging
import os
from dotenv import load_dotenv
from telegram import Update
from src.services.gemini_service import gemini
from src.services.file_manager import file_manager
from src.services.calendar_service import calendar
from src.services.odoo_service import odoo
from src.services.job_service import job_service
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, TypeHandler, ApplicationHandlerStop

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

async def auth_middleware(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Authentication middleware to restrict access to the allowed user."""
    if not update.effective_user:
        # Fail closed for updates without an effective user (e.g., channel posts)
        raise ApplicationHandlerStop()

    allowed_user_id_str = os.getenv("ALLOWED_USER_ID")
    if not allowed_user_id_str:
        logger.error("ALLOWED_USER_ID n'est pas configuré. Accès refusé par défaut.")
        raise ApplicationHandlerStop()

    try:
        allowed_user_id = int(allowed_user_id_str)
    except ValueError:
        logger.error("ALLOWED_USER_ID doit être un nombre entier. Accès refusé par défaut.")
        raise ApplicationHandlerStop()

    if update.effective_user.id != allowed_user_id:
        logger.warning(f"Accès non autorisé de l'utilisateur {update.effective_user.id} ({update.effective_user.username})")
        # Optional: notify the unauthorized user
        if update.effective_message:
            try:
                await update.effective_message.reply_text("⛔ Accès non autorisé. Ce bot est privé.")
            except Exception:
                pass
        raise ApplicationHandlerStop()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f"Bonjour {user.first_name} ! Je suis votre assistant personnel.\n\n"
        "Je peux vous aider avec :\n"
        "📅 /agenda - Gérer votre agenda et rappels\n"
        "📁 /fichiers - Classer et ranger vos documents\n"
        "💶 /compta - Gérer votre comptabilité (Odoo, dépenses)\n"
        "💼 /emplois - Chercher des emplois au Luxembourg\n\n"
        "Comment puis-je vous aider aujourd'hui ?"
    )
    await update.message.reply_text(welcome_message)

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

    try:
        # Check if the user is asking to add an event
        if "ajouter" in text.lower() and ("rendez-vous" in text.lower() or "agenda" in text.lower() or "formation" in text.lower()):
            prompt = f"L'utilisateur veut ajouter un événement à son agenda: '{text}'. Extrais le Titre de l'événement et la Date (format compréhensible comme 'Demain à 14h' ou 'Le 25 Juin'). Réponds STRICTEMENT sous ce format: Titre | Date. Exemple: Formation Python | Lundi 15 Mars à 10h."
            extraction = gemini.generate_response(prompt)
            parts = extraction.split('|')
            if len(parts) >= 2:
                result = calendar.add_event(parts[0].strip(), parts[1].strip())
                await update.message.reply_text(result)
            else:
                await update.message.reply_text(f"Désolé, je n'ai pas pu extraire la date correctement. Résultat IA: {extraction}")
            return

        # Check if user wants to add an expense
        if "dépens" in text.lower() or "payé" in text.lower() or "acheté" in text.lower():
            prompt = f"L'utilisateur vient d'indiquer une dépense: '{text}'. Extrais le Motif de l'achat et le Montant (avec la devise). Réponds STRICTEMENT sous ce format: Motif | Montant. Exemple: Restaurant O'Tacos | 15.50€."
            extraction = gemini.generate_response(prompt)
            parts = extraction.split('|')
            if len(parts) >= 2:
                result = odoo.add_expense(parts[0].strip(), parts[1].strip())
                await update.message.reply_text(result)
            else:
                await update.message.reply_text("Je n'ai pas pu comprendre le montant ou le motif. Veuillez réessayer.")
            return

        # Check if user wants a cover letter
        if "lettre de motivation" in text.lower() or "postuler" in text.lower():
            # Very basic check, assuming the user just pastes the job description
            await update.message.reply_text("Je rédige votre lettre de motivation...")
            response = gemini.generate_cover_letter(text, "Profil Polyvalent et Motivé") # In a real scenario, fetch CV summary
            await update.message.reply_text(response)
            return

        # General conversational response
        await update.message.chat.send_action("typing")
        response = gemini.generate_response(text)
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

    # Register the authentication middleware globally (executes before other handlers)
    application.add_handler(TypeHandler(Update, auth_middleware), group=-1)

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Placeholder commands for the modules

    application.add_handler(CommandHandler("agenda", agenda_command))
    application.add_handler(CommandHandler("fichiers", fichiers_command))

    application.add_handler(CommandHandler("compta", compta_command))
    application.add_handler(CommandHandler("emplois", emplois_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    logger.info("Démarrage du bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
