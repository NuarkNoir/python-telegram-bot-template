# This module contains different things you may need
from functools import wraps
from config import Config


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in Config.LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def mention_user(tg_user_id: int, tg_first_name: str, tg_last_name: str = "", tg_username: str = "") -> str:
    tpl_mstr = "[{0}](tg://user?id={1})"
    ment_str = ""

    if tg_first_name:
        ment_str += tg_first_name
    if tg_username:
        ment_str += f" '{tg_username}'"
    if tg_last_name:
        ment_str += " " + tg_last_name

    return tpl_mstr.format(ment_str, tg_user_id)


def mention_post(group_id, message_id) -> str:
    return f"[{group_id}/{message_id}](https://t.me/{group_id}/{message_id})"


def pluralize(quantity: int, singular: str, plural: str = "") -> str:
    if quantity == 1 or not len(singular):
        return singular
    if plural:
        return plural

    last_letter = singular[-1].lower()
    if last_letter == "y":
        return singular[:-1] + "ies"
    elif last_letter == "s":
        return singular + "es"
    else:
        return singular + "s"


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu
