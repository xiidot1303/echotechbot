from bot.bot import *
from bot.bot.promocode import _to_the_getting_promocode

async def promocode(update: Update, context: CustomContext):
    # to the getting promocode
    return await _to_the_getting_promocode(update)

async def terms_of_action(update: Update, context: CustomContext):
    # identidy lang of the user
    bot_user: Bot_user = await get_object_by_update(update) 
    obj = await TermOfElectric.objects.aget(pk=1)
    if bot_user.lang == 'uz':
        file = obj.file_uz
    else:
        file = obj.file_ru
    await bot_send_document(update, context, document=file)
    return

async def prizes(update: Update, context: CustomContext):
    # identidy lang of the user
    bot_user: Bot_user = await get_object_by_update(update) 
    obj = await Prize.objects.aget(pk=1)
    if bot_user.lang == 'uz':
        file = obj.file_uz
    else:
        file = obj.file_ru
    await bot_send_document(update, context, document=file)
    return