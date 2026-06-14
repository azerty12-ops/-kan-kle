import logging
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from src.services.gemini_service import gemini
from src.services.file_manager import file_manager
from src.services.calendar_service import calendar
from src.services.odoo_service import odoo
from src.services.job_service import job_service
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, TypeHandler, ApplicationHandlerStop

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_ID = os.getenv("ALLOWED_USER_ID")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def auth_middleware(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Authentication middleware to block unauthorized users."""
    if not ALLOWED_USER_ID:
        return # Skip auth if not configured

    user = update.effective_user
    if user and str(user.id) != ALLOWED_USER_ID:
        logger.warning(f"Unauthorized access attempt by user {user.id} ({user.username})")
        if update.message:
            await update.message.reply_text("Désolé, vous n'êtes pas autorisé à utiliser ce bot.")
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
    keyboard = [
        ["/agenda", "/fichiers"],
        ["/compta", "/emplois"]
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

    try:
        await update.message.chat.send_action("typing")
        intent = await gemini.analyze_intent_async(text)

        if intent == "AGENDA":
            prompt = f"L'utilisateur veut ajouter un événement à son agenda ou a posé une question sur son agenda: '{text}'. S'il veut l'ajouter, extrais le Titre de l'événement et la Date (format compréhensible comme 'Demain à 14h' ou 'Le 25 Juin'). Réponds STRICTEMENT sous ce format: Titre | Date. S'il ne veut pas ajouter, réponds par NON."
            extraction = await gemini.generate_response_async(prompt)
            if extraction.strip() != "NON":
                parts = extraction.split('|')
                if len(parts) >= 2:
                    result = calendar.add_event(parts[0].strip(), parts[1].strip())
                    await update.message.reply_text(result)
                    return
            response = await gemini.generate_response_async(f"Tu es l'assistant de l'utilisateur. Réponds à sa question concernant l'agenda : {text}")
            await update.message.reply_text(response)

        elif intent == "COMPTA":
            prompt = f"L'utilisateur vient d'indiquer une dépense ou parle de comptabilité: '{text}'. S'il s'agit d'une nouvelle dépense, extrais le Motif de l'achat et le Montant (avec la devise). Réponds STRICTEMENT sous ce format: Motif | Montant. Exemple: Restaurant O'Tacos | 15.50€. S'il ne s'agit pas d'une dépense à ajouter, réponds par NON."
            extraction = await gemini.generate_response_async(prompt)
            if extraction.strip() != "NON":
                parts = extraction.split('|')
                if len(parts) >= 2:
                    result = odoo.add_expense(parts[0].strip(), parts[1].strip())
                    await update.message.reply_text(result)
                    return
            response = await gemini.generate_response_async(f"Tu es l'assistant de l'utilisateur. Réponds à sa question concernant la comptabilité : {text}")
            await update.message.reply_text(response)

        elif intent == "EMPLOI":
            await update.message.reply_text("Je rédige votre lettre de motivation...")
            response = await gemini.generate_cover_letter_async(text, "Profil Polyvalent et Motivé")
            await update.message.reply_text(response)

        elif intent == "FICHIERS":
             await fichiers_command(update, context)

        else:
            # General conversational response (CHAT or fallback)
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

    # Authentication middleware
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
