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
    main, login, businessman, electric, promocode
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

promocode_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Text(lang_dict['enter promocode']), electric.promocode)
    ],
    states={
        GET_PROMOCODE: [
            MessageHandler(filters.TEXT & exceptions_for_filter_text, promocode.get_promocode)
        ],
    }, 
    fallbacks=[
        CommandHandler("start", promocode.start),
        MessageHandler(filters.Text(lang_dict['main menu']), promocode.start)
    ]
)

main_menu_button = MessageHandler(filters.Text(lang_dict['main menu']), main.main_menu)
products_handler = MessageHandler(filters.Text(lang_dict['products']), main.products)
dealers_handler = MessageHandler(filters.Text(lang_dict['dilers']), main.dealers)
action_for_businessman_handler = MessageHandler(filters.Text(lang_dict['action for businessman']), businessman.terms_of_action)
# electric
action_for_electric_handler = MessageHandler(filters.Text(lang_dict['action for electric']), main.action_for_electric)
terms_of_electric_handler = MessageHandler(filters.Text(lang_dict['terms of action']), electric.terms_of_action)
prizes_handler = MessageHandler(filters.Text(lang_dict['prizes']), electric.prizes)
my_points_handler = MessageHandler(filters.Text(lang_dict['my points']), electric.my_points)
top20_handler = CallbackQueryHandler(electric.top20, pattern='top20')


handlers = [
    login_handler,
    main_menu_button, 
    products_handler,
    dealers_handler,
    action_for_businessman_handler,
    action_for_electric_handler,
    promocode_handler,
    terms_of_electric_handler,
    prizes_handler,
    my_points_handler,
    top20_handler,
    
]