# This module contains all your bot action handlers definition
# Also there is run() and stop() functions to start and
# stop bot, but you are not really gonna call them by hand
import sys
import traceback

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler
from telegram.ext.messagequeue import MessageQueue
from telegram.utils.helpers import mention_html
from telegram.utils.request import Request

from config import Config
from internals.bot import MQBot
from database.db import db_handle, stop_db
from internals.actions import send_typing_action


def error_callback(update, context):
    trace = "".join(traceback.format_tb(sys.exc_info()[2]))
    payload = ""
    if update.effective_user:
        payload += f" with the user {mention_html(update.effective_user.id, update.effective_user.first_name)}"

    if update.effective_chat:
        payload += f" within the chat <b>{update.effective_chat.title}</b>"
        if update.effective_chat.username:
            payload += f" (@{update.effective_chat.username})"

    if update.poll:
        payload += f" with the poll id {update.poll.id}."

    text = (f"Hey. The error <pre>{context.error}</pre> happened {payload}. "
            f"The full traceback:\n\n<pre>{trace}</pre>")

    for dev_id in Config.LIST_OF_ADMINS:
        context.bot.send_message(dev_id, text, parse_mode=ParseMode.HTML)
    raise


@send_typing_action
def start(update: Update, context):
    """ /start command handler """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello there",
        isgroup=False
    )


mq = MessageQueue(
    all_burst_limit=29, all_time_limit_ms=1020,
    group_burst_limit=10, group_time_limit_ms=40000
)
request = Request(con_pool_size=1)
bot_worker = MQBot(Config.TOKEN, request=request, mqueue=mq)
updater = Updater(bot=bot_worker, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_error_handler(error_callback)


def run():
    db_handle.start()
    updater.start_polling()
    updater.idle()


def stop():
    if not stop_db():
        print("Cannot stop database")
    mq.stop()
    updater.stop()
