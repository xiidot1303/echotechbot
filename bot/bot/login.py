from bot.bot import *
from app.services import *
from bot.bot.electric import electric_main_menu as _electric_main_menu

async def _to_the_select_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update_message_reply_text(
        update,
        "Bot tilini tanlang\n\nВыберите язык бота",
        reply_markup= await select_lang_keyboard()
    )
    return GET_LANG

async def _to_the_getting_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update_message_reply_text(
        update, 
        await get_word("type name", update),
        reply_markup = await reply_keyboard_markup([[await get_word("back", update)]])
    )
    return GET_NAME

async def _to_the_getting_contact(update: Update):
    i_contact = KeyboardButton(
        text=await get_word("leave number", update),
        request_contact=True
    )

    await update_message_reply_text(
        update,
        await get_word("send number", update),
        reply_markup=await reply_keyboard_markup(
            [[i_contact], [await get_word("back", update)]],
        )
    )

    return GET_CONTACT

async def _to_the_getting_region(update: Update, context: CustomContext):
    i_buttons = [
        InlineKeyboardButton(
            text=await get_word(region[0], update),
            callback_data=f"select_region-{region[0]}"
        )
        for region in Bot_user.REGION_CHOICES
    ]
    i_buttons_split = [i_buttons[i:i + 2] for i in range(0, len(i_buttons), 2)]
    markup = InlineKeyboardMarkup(i_buttons_split)
    text = await get_word('choose region', update)
    message = await update_message_reply_text(update, text, reply_markup=await reply_keyboard_remove())
    await bot_send_message(update, context, "👇", reply_markup=markup)
    return GET_REGION

async def _to_the_getting_address(update: Update):
    text = await get_word('type address', update)
    markup = await build_keyboard(update, [], 2)
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_ADDRESS

###################################################################################
###################################################################################

async def get_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "UZ" in text:
        lang = 'uz'
    elif "RU" in text:
        lang = 'ru'
    else:
        return await _to_the_select_lang(update, context)

    await get_or_create(user_id=update.message.chat_id)
    obj = await get_object_by_user_id(user_id=update.message.chat_id)
    obj.lang = lang
    await obj.asave()

    # end conversation
    await main_menu(update, context)
    return ConversationHandler.END
    # return await _to_the_getting_name(update, context)

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await is_message_back(update):
        await main_menu(update, context)
        return ConversationHandler.END

    obj = await get_object_by_update(update)
    obj.name = update.message.text
    obj.username = update.message.chat.username
    obj.firstname = update.message.chat.first_name
    await obj.asave()

    return await _to_the_getting_contact(update)

async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await is_message_back(update):
        return await _to_the_getting_name(update, context)

    # get phone number from contact or message text
    if c := update.message.contact:
        phone_number = c.phone_number
    else:
        phone_number = update.message.text

    # check phone number is registred in the past or not
    is_available = await filter_objects_sync(Bot_user, {'phone': phone_number})
    if is_available:
        await update.message.reply_text(
            await get_word("number is logged", update)
        )
        return GET_CONTACT
    
    obj = await get_object_by_update(update)
    obj.phone = phone_number
    await obj.asave()

    return await _to_the_getting_region(update, context)

async def get_region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query: CallbackQuery = update.callback_query
    # get region from callback query data
    data = query.data
    *args, region = data.split('-')
    # get bot user
    bot_user: Bot_user = await get_object_by_update(query)
    # set region to bot_user
    bot_user.region = region
    await bot_user.asave()
    await query.answer()
    await bot_edit_message_reply_markup(query, context, reply_markup=None)
    return await _to_the_getting_address(query)

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await is_message_back(update):
        return await _to_the_getting_region(update, context)
    
    address = update.message.text
    bot_user: Bot_user = await get_object_by_update(update)
    bot_user.address = address
    await bot_user.asave()
    await _electric_main_menu(update, context)
    return ConversationHandler.END



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await _to_the_select_lang(update, context)