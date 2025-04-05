from bot.bot import *
from app.services.promocode_service import *
from app.services.statement_service import *

async def _to_the_getting_promocode(update: Update, context: CustomContext = None):
    text = await get_word('type promocode', update)
    markup = await build_keyboard(update, [], 2, back_button=False)
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_PROMOCODE


async def to_the_getting_photo(update: Update):
    text = await get_word('send photo', update)
    markup = await build_keyboard(update, [await get_word('confirm', update)], 2, back_button=True, main_menu_button=False)
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_PHOTO

#########################################################################

async def get_promocode(update: Update, context: CustomContext):
    # get promocode from message text
    code = update.message.text
    # check that this promocode is available or not
    if promocode := await get_unused_promocode_by_code(code):
        context.user_data['promocode_id'] = promocode.id
        return await to_the_getting_photo(update)
    else:
        # send message that promocode is not valid
        text = await get_word('promocode is not valid', update)
        await update_message_reply_text(update, text)


async def get_photo(update: Update, context: CustomContext):
    # get photo from message
    photo = await save_and_get_photo(update, context)
    photos: list = context.user_data.get('photos', [])
    photos.append(photo)
    context.user_data['photos'] = photos
    return


async def confirm_photos(update: Update, context: CustomContext):
    # get promocode id from user_data
    promocode_id = context.user_data.get('promocode_id')
    photos = context.user_data.get('photos', None)
    if not photos:
        return await to_the_getting_photo(update)

    # create statement
    statement = await create_statement(update.effective_user.id, promocode_id, photos)
    photos = context.user_data.pop('photos')
    if not statement:
        # send message that statement is not accepted
        text = await get_word('statement not accepted', update)
        await update_message_reply_text(update, text)
        return await _to_the_getting_promocode(update)
        
    # send message that statement is accepted
    text = await get_word('statement accepted', update)
    await update_message_reply_text(update, text)
    await main_menu(update, context)
    return ConversationHandler.END


async def start(update: Update, context: CustomContext):
    await main_menu(update, context)
    return ConversationHandler.END