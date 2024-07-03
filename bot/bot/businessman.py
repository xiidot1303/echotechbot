from bot.bot import *
from bot.models import TermOfBusinessman

async def terms_of_action(update: Update, context: CustomContext):
    # identidy lang of the user
    bot_user: Bot_user = await get_object_by_update(update) 
    obj = await TermOfBusinessman.objects.aget(pk=1)
    if bot_user.lang == 'uz':
        file = obj.file_uz
    else:
        file = obj.file_ru
    text = await get_word('terms of action', update)
    await update_message_reply_text(update, text)
    await bot_send_document(update, context, document=file)
    return