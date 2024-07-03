from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    InlineQueryHandler,
    TypeHandler,
    ConversationHandler
)

from bot.resources.strings import lang_dict
from bot.resources.conversationList import *

from bot.bot import (
    main, login, businessman
)

exceptions_for_filter_text = (~filters.COMMAND) & (~filters.Text(lang_dict['main menu']))

login_handler = ConversationHandler(
    entry_points=[CommandHandler("start", main.start)],
    states={
        GET_LANG: [
            MessageHandler(filters.Text(lang_dict["uz_ru"]), login.get_lang),
            MessageHandler(filters.TEXT & (~filters.COMMAND), login.get_lang)
        ],
        GET_NAME: [
            MessageHandler(filters.TEXT & (~filters.COMMAND), login.get_name)
        ],
        GET_CONTACT: [
            MessageHandler(filters.CONTACT, login.get_contact),
            MessageHandler(filters.Text(lang_dict['back']), login.get_contact),
            MessageHandler(filters.TEXT & (~filters.COMMAND), login.get_contact)
        ]
    },
    fallbacks=[
        CommandHandler("start", login.start)
    ],
    name="login",
)

main_menu_button = MessageHandler(filters.Text(lang_dict['main menu']), main.main_menu)
products_handler = MessageHandler(filters.Text(lang_dict['products']), main.products)
dealers_handler = MessageHandler(filters.Text(lang_dict['dilers']), main.dealers)
action_for_businessman_handler = MessageHandler(filters.Text(lang_dict['action for businessman']), businessman.terms_of_action)

handlers = [
    login_handler,
    main_menu_button, 
    products_handler,
    dealers_handler,
    action_for_businessman_handler,
    
]