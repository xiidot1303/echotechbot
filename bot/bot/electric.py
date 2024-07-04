from bot.bot import *
from bot.bot.promocode import _to_the_getting_promocode
import config
from asgiref.sync import sync_to_async

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

async def my_points(update: Update, context: CustomContext):
    user: Bot_user = await get_user_by_update(update)
    user_point = user.point
    statistic_url = config.WEBHOOK_URL + "/statistic"
    # points = Request.objects.filter(user = user).values('user__name').annotate(p=Sum(F('point')*F('amount')))[0]['p']
    msg = '<b>{}</b>: {}'.format(await get_word('your points', update), user_point)
    msg += '\n\n👉 <a href="{}">🔗{}</a> 👈'.format(statistic_url, await get_word('action results', update))
    i_top20 = InlineKeyboardButton(text=await get_word('top20', update), callback_data='top20')
    markup = InlineKeyboardMarkup([[i_top20]])
    await update_message_reply_text(update, msg, reply_markup = markup)


async def top20(update: Update, context: CustomContext):
    update = update.callback_query
    if update.data == 'top20':
        current_user = await get_user_by_update(update)
        query_users = Bot_user.objects.filter().exclude(phone=None).order_by('-point')
        list_users = await sync_to_async(list)(query_users.values_list('pk', flat=True))
        top20_list = query_users[:20]
        user_index = list_users.index(current_user.pk) + 1
    
        message = '⬆️ Top 20:\n\n'
        n = 1
        async for user in top20_list:
            text = ''
            if n == 1:
                text += '1️⃣. '
            elif n == 2:
                text += '2️⃣. '
            elif n == 3:
                text += '3️⃣. '
            else:
                text += '{}. '.format(n)

            text += '{}➖{}\n'.format(user.name, user.point)
            if user == current_user:
                text = '<u><b>{}</b></u>'.format(text)
            message += text
            n += 1
    
        if user_index > 20:
            if user_index != 21:
                message += '....\n'
            message += '{}. {}➖{}'.format(user_index, current_user.name, user.point)
        await update_message_reply_text(update, message)
        await update.answer()