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
    },
    fallbacks=[
        CommandHandler("start", login.start)
    ],
    name="login",
    persistent=True
)

action_for_electric_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Text(lang_dict['action for electric']), main.action_for_electric)],
    states={
        GET_NAME: [
            MessageHandler(filters.TEXT & exceptions_for_filter_text, login.get_name)
        ],
        GET_CONTACT: [
            MessageHandler(filters.CONTACT, login.get_contact),
            MessageHandler(filters.Text(lang_dict['back']), login.get_contact),
            MessageHandler(filters.TEXT & exceptions_for_filter_text, login.get_contact)
        ],
        GET_REGION: [
            CallbackQueryHandler(login.get_region, pattern=r"^select_region")
        ],
        GET_ADDRESS: [
            MessageHandler(filters.TEXT & exceptions_for_filter_text, login.get_address)

        ]

    },
    fallbacks=[
        CommandHandler("start", promocode.start),
        MessageHandler(filters.Text(lang_dict['main menu']), promocode.start)
    ],
    name='action_for_electric',
    persistent=True

)

promocode_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Text(lang_dict['enter promocode']), electric.promocode)
    ],
    states={
        GET_PROMOCODE: [
            MessageHandler(filters.TEXT & exceptions_for_filter_text, promocode.get_promocode)
        ],
        GET_PHOTO: [
            MessageHandler(filters.PHOTO, promocode.get_photo),
            MessageHandler(filters.Text(lang_dict['back']), promocode._to_the_getting_promocode),
            MessageHandler(filters.Text(lang_dict['confirm']), promocode.confirm_photos)
        ]
    }, 
    fallbacks=[
        CommandHandler("start", promocode.start),
        MessageHandler(filters.Text(lang_dict['main menu']), promocode.start)
    ],
    name="promocode",
    persistent=True
)

main_menu_button = MessageHandler(filters.Text(lang_dict['main menu']), main.main_menu)
products_handler = MessageHandler(filters.Text(lang_dict['products']), main.products)
dealers_handler = MessageHandler(filters.Text(lang_dict['dilers']), main.dealers)
action_for_businessman_handler = MessageHandler(filters.Text(lang_dict['action for businessman']), businessman.terms_of_action)
# electric
terms_of_electric_handler = MessageHandler(filters.Text(lang_dict['terms of action']), electric.terms_of_action)
prizes_handler = MessageHandler(filters.Text(lang_dict['prizes']), electric.prizes)
my_tickets_handler = MessageHandler(filters.Text(lang_dict['my tickets']), electric.my_tickets)
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
    my_tickets_handler,
    my_points_handler,
    top20_handler,
    
]