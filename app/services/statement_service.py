from app.services import *
from app.models import Statement, Photo
from app.services.promocode_service import *
from bot.services import *
from bot.services.string_service import *
from django.db.utils import IntegrityError


async def statement_confirm(instance):
    promocode = await instance.get_promocode
    # set promocode as used
    await promocode.set_as_used()
    # add points to user
    bot_user: Bot_user = await instance.get_bot_user
    await bot_user.add_point(10)
    # create user promocode
    user_promocode: UserPromoCode = await create_user_promocode(bot_user, promocode)
    
    # send successful message to user
    text = await promocode_accepted_string(bot_user.user_id, user_promocode.id)
    from bot.control.updater import application
    await application.bot.send_message(bot_user.user_id, text, parse_mode='HTML')


async def statement_deleted(instance):
    bot_user: Bot_user = await instance.get_bot_user
    # send cancellation message to user
    text = await get_word('statement canceled', chat_id=bot_user.user_id)
    from bot.control.updater import application
    await application.bot.send_message(bot_user.user_id, text, parse_mode='HTML')


async def create_statement(user_id, promocode_id, photos) -> Statement | None:
    bot_user = await get_object_by_user_id(user_id)
    promocode = await PromoCode.objects.aget(id=promocode_id)
    try:
        statement = await Statement.objects.acreate(bot_user=bot_user, promocode=promocode)
        # create photos
        photos_to_create = [
            Photo(
                file = photo,
                statement = statement
            ) for photo in photos
        ]
        await Photo.objects.abulk_create(photos_to_create)
    except IntegrityError:
        return None

    return statement