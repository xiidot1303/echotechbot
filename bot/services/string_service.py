from bot.services.language_service import *

async def promocode_accepted_string(update, user_promocode_id):
    text = f"{await get_word('promocode accepted successfully', update)}\n" \
        f"{await get_word('your special id', update)}: <b>№ {user_promocode_id}</b>." \
            f"{await get_word('use it in competition', update)}"
    return text

async def tickets_list_string(userpromocodes):
    text = ""
    async for userpromocode in userpromocodes:
        line_text = f"№ <code><b>{userpromocode.pk}</b></code>" \
            f" - {userpromocode.entered_at.strftime('%d.%m.%Y')}\n"
        text += line_text
    return text
