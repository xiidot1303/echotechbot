from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes, CallbackContext, ExtBot
from dataclasses import dataclass
from asgiref.sync import sync_to_async
from bot.utils import *
from bot.utils.bot_functions import *
from bot.utils.keyboards import *
from bot.resources.strings import lang_dict
from bot.services import *
from bot.services.language_service import *
from bot.services.string_service import *
from bot.resources.conversationList import *
from config import WEBAPP_URL

@dataclass
class WebhookUpdate:
    """Simple dataclass to wrap a custom update type"""
    user_id: int
    payload: str

class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    @classmethod
    def from_update(
        cls,
        update: object,
        application: "Application",
    ) -> "CustomContext":
        if isinstance(update, WebhookUpdate):
            return cls(application=application, user_id=update.user_id)
        return super().from_update(update, application)


async def is_message_back(update: Update):
    if update.message.text == await get_word("back", update):
        return True
    else:
        return False

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update = update.callback_query if update.callback_query else update

    bot = context.bot
    words = ['products', 'dilers', 'action for electric', 'action for businessman']

    keyboards = [
        await get_word(word, update)
        for word in words
    ]
    markup = await build_keyboard(update, keyboards, 2, back_button=False, main_menu_button=False)
    await bot.send_message(
        update.message.chat_id,
        await get_word('main menu', update),
        reply_markup=markup
    )

    await check_username(update)