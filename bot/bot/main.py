from bot.bot import *
from bot.models import *
from bot.bot.login import _to_the_getting_name
from bot.bot.electric import electric_main_menu

async def start(update: Update, context: CustomContext):
    if await is_group(update):
        return
    
    if await is_registered(update.message.chat.id):
        # main menu
        await main_menu(update, context)
        return
    else:
        hello_text = lang_dict['hello']
        await update_message_reply_text(
            update,
            hello_text,
            reply_markup= await select_lang_keyboard()
        )
        return GET_LANG

async def products(update: Update, context: CustomContext):
    # identidy lang of the user
    bot_user: Bot_user = await get_object_by_update(update)
    # get products file
    product_file_obj: ProductsFile = await ProductsFile.objects.aget(pk=1)
    if bot_user.lang == 'uz':
        product_file = product_file_obj.file_uz
    else:
        product_file = product_file_obj.file_ru
    await bot_send_document(update, context, document=product_file)
    return

async def dealers(update: Update, context: CustomContext):
    # identidy lang of the user
    bot_user: Bot_user = await get_object_by_update(update)
    # get dealer object
    dealer_obj = await Diler.objects.aget(pk=1)
    if bot_user.lang == 'uz':
        text = dealer_obj.text_uz
    else:
        text = dealer_obj.text_ru
    await update_message_reply_text(update, text)
    return

async def action_for_businessman(update: Update, context: CustomContext):
    keyboards = [await get_word('terms of action', update)]
    markup = await build_keyboard(update, keyboards, 2, back_button=False)
    text = await get_word('action for businessman', update)
    await update_message_reply_text(update, text, reply_markup=markup)
    return

async def action_for_electric(update: Update, context: CustomContext):
    bot_user: Bot_user = await get_object_by_update(update)
    # if user is not registred fully, redirect it to the getting name
    if not bot_user.phone:
        return await _to_the_getting_name(update, context)

    await electric_main_menu(update, context)