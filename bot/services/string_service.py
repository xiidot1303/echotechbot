from bot.services.language_service import *

async def promocode_accepted_string(user_id, user_promocode_id):
    text = f"{await get_word('promocode accepted successfully', chat_id=user_id)}\n" \
        f"{await get_word('your special id', chat_id=user_id)}: <b>№ {user_promocode_id}</b>." \
            f"{await get_word('use it in competition', chat_id=user_id)}"
    return text

async def tickets_list_string(userpromocodes):
    text = ""
    async for userpromocode in userpromocodes:
        line_text = f"№ <code><b>{userpromocode.pk}</b></code>" \
            f" - {userpromocode.entered_at.strftime('%d.%m.%Y')}\n"
        text += line_text
    return text
