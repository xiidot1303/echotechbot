from app.services import *
from app.models import PromoCode, UserPromoCode
from bot.models import Bot_user

def promocodes_all():
    query = PromoCode.objects.filter()
    return query

async def create_promocodes(codes):
    promo_codes = [PromoCode(code=code) for code in codes]
    await PromoCode.objects.abulk_create(promo_codes)

async def get_unused_promocode_by_code(code) -> PromoCode | None:
    try:
        obj = await PromoCode.objects.aget(
            code = code, used = False
        )
        return obj
    except PromoCode.DoesNotExist:
        return None
    
async def create_user_promocode(bot_user: Bot_user, promocode: PromoCode) -> UserPromoCode:
    obj = await UserPromoCode.objects.acreate(user = bot_user, promo_code = promocode)
    return obj