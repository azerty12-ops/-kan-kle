import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from telegram import Update, User, Message, Chat
from telegram.ext import ContextTypes, ApplicationHandlerStop
from src.bot.main import auth_middleware, handle_message

@pytest.mark.asyncio
async def test_auth_middleware_authorized():
    update = MagicMock(spec=Update)
    update.effective_user = MagicMock(spec=User)
    update.effective_user.id = 12345
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    with patch('src.bot.main.ALLOWED_USER_ID', '12345'):
        # Should not raise any exception
        await auth_middleware(update, context)

@pytest.mark.asyncio
async def test_auth_middleware_unauthorized():
    update = MagicMock(spec=Update)
    update.effective_user = MagicMock(spec=User)
    update.effective_user.id = 54321
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    with patch('src.bot.main.ALLOWED_USER_ID', '12345'):
        with pytest.raises(ApplicationHandlerStop):
            await auth_middleware(update, context)

@pytest.mark.asyncio
async def test_handle_message_agenda_intent():
    update = MagicMock(spec=Update)
    update.message = AsyncMock(spec=Message)
    update.message.text = "voir agenda"
    update.message.chat = MagicMock(spec=Chat)
    update.message.chat.send_action = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    with patch('src.bot.main.gemini.analyze_intent_async', new_callable=AsyncMock) as mock_analyze:
        with patch('src.bot.main.gemini.generate_response_async', new_callable=AsyncMock) as mock_generate:
            with patch('src.bot.main.calendar.get_upcoming_events', return_value="Events"):
                mock_analyze.return_value = "AGENDA"
                mock_generate.return_value = "GET_AGENDA"

                await handle_message(update, context)

                update.message.reply_text.assert_called_with("Events")

@pytest.mark.asyncio
async def test_handle_message_compta_intent():
    update = MagicMock(spec=Update)
    update.message = AsyncMock(spec=Message)
    update.message.text = "voir compta"
    update.message.chat = MagicMock(spec=Chat)
    update.message.chat.send_action = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    with patch('src.bot.main.gemini.analyze_intent_async', new_callable=AsyncMock) as mock_analyze:
        with patch('src.bot.main.gemini.generate_response_async', new_callable=AsyncMock) as mock_generate:
            with patch('src.bot.main.odoo.get_recent_invoices', return_value="Invoices"):
                mock_analyze.return_value = "COMPTA"
                mock_generate.return_value = "GET_COMPTA"

                await handle_message(update, context)

                update.message.reply_text.assert_called_with("Invoices")
