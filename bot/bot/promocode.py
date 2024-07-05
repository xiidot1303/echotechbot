from bot.bot import *
from app.services.promocode_service import *

async def _to_the_getting_promocode(update: Update):
    text = await get_word('type promocode', update)
    markup = await build_keyboard(update, [], 2, back_button=False)
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_PROMOCODE

#########################################################################

async def get_promocode(update: Update, context: CustomContext):
    # get promocode from message text
    code = update.message.text
    # check that this promocode is available or not
    if promocode := await get_unused_promocode_by_code(code):
        # set promocode as used
        await promocode.set_as_used()
        # add points to user
        bot_user: Bot_user = await get_object_by_update(update)
        await bot_user.add_point(10)
        # create user promocode
        user_promocode: UserPromoCode = await create_user_promocode(bot_user, promocode)
        
        # send successfull message to user
        text = await promocode_accepted_string(update, user_promocode.id)
        await update_message_reply_text(update, text)
        await main_menu(update, context)
        return ConversationHandler.END

    else:
        # send message that promocode is not valid
        text = await get_word('promocode is not valid', update)
        await update_message_reply_text(update, text)

async def start(update: Update, context: CustomContext):
    await main_menu(update, context)
    return ConversationHandler.END