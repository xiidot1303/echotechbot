from bot.services.language_service import *

async def promocode_accepted_string(update, user_promocode_id):
    text = f"{await get_word('promocode accepted successfully', update)}\n" \
        f"{await get_word('your special id', update)}: <b>№ {user_promocode_id}</b>." \
            f"{await get_word('use it in competition', update)}"
    return text