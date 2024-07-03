from app.services import *
from app.models import PromoCode, UserPromoCode

def promocodes_all():
    query = PromoCode.objects.filter()
    return query

async def create_promocodes(codes):
    promo_codes = [PromoCode(code=code) for code in codes]
    await PromoCode.objects.abulk_create(promo_codes)