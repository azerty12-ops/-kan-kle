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
        await update.message.chat.send_action("typing")
        intent = await gemini.analyze_intent(text)

        if "AGENDA" in intent:
            prompt = f"L'utilisateur veut interagir avec son agenda: '{text}'. Si c'est pour ajouter un événement, extrais 'AJOUTER | Titre | Date'. Sinon, réponds 'VOIR'."
            action = await gemini.generate_response(prompt)
            if "AJOUTER" in action:
                parts = action.split('|')
                if len(parts) >= 3:
                    result = calendar.add_event(parts[1].strip(), parts[2].strip())
                    await update.message.reply_text(result)
                else:
                    await update.message.reply_text(f"Désolé, je n'ai pas pu extraire la date correctement. Résultat IA: {action}")
            else:
                await agenda_command(update, context)

        elif "COMPTA" in intent:
            prompt = f"L'utilisateur veut interagir avec sa compta: '{text}'. Si c'est pour ajouter une dépense, extrais 'AJOUTER | Motif | Montant'. Sinon, réponds 'VOIR'."
            action = await gemini.generate_response(prompt)
            if "AJOUTER" in action:
                parts = action.split('|')
                if len(parts) >= 3:
                    result = odoo.add_expense(parts[1].strip(), parts[2].strip())
                    await update.message.reply_text(result)
                else:
                    await update.message.reply_text("Je n'ai pas pu comprendre le montant ou le motif. Veuillez réessayer.")
            else:
                await compta_command(update, context)

        elif "FICHIERS" in intent:
            await fichiers_command(update, context)

        elif "EMPLOI" in intent:
            if "lettre" in text.lower() or "motivation" in text.lower() or "postuler" in text.lower():
                await update.message.reply_text("Je rédige votre lettre de motivation...")
                response = await gemini.generate_cover_letter(text, "Profil Polyvalent et Motivé")
                await update.message.reply_text(response)
            else:
                prompt = f"Extrais le métier ou mot-clé de recherche d'emploi de ce message: '{text}'. Si non trouvé, réponds 'comptable'."
                keyword = await gemini.generate_response(prompt)
                context.args = [keyword.strip()]
                await emplois_command(update, context)

        else:
            response = await gemini.generate_response(text)
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

async def check_allowed_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Authentication middleware to block unauthorized users."""
    if not update.effective_user:
        return

    allowed_user_id_str = os.getenv("ALLOWED_USER_ID")

    try:
        if not allowed_user_id_str:
            raise ValueError()
        allowed_user_id = int(allowed_user_id_str)
    except (ValueError, TypeError):
        raise ApplicationHandlerStop()

    if update.effective_user.id != allowed_user_id:
        raise ApplicationHandlerStop()

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    if not TOKEN or TOKEN == "votre_token_telegram_ici":
        logger.error("Veuillez configurer TELEGRAM_BOT_TOKEN dans le fichier .env")
        return

    application = Application.builder().token(TOKEN).build()

    # Authentication middleware
    application.add_handler(TypeHandler(Update, check_allowed_user), group=-1)

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
