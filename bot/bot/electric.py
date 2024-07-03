from bot.bot import *
from bot.bot.promocode import _to_the_getting_promocode

async def promocode(update: Update, context: CustomContext):
    # to the getting promocode
    return await _to_the_getting_promocode(update)
