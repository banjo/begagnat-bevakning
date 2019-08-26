import os
from telegram.ext import Updater

TELEGRAM_API = os.environ.get("TELEGRAM_KEY")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# setup telegram variables
updater = Updater(TELEGRAM_API)
bot = updater.bot
# chat_id = bot.get_updates()[-1].message.chat_id


def send_blocket_to_telegram(article):
    # create string
    string = f"""
Blocket
{article["title"]}
{article["place"]}
{article["time"]}
{article["price"]}
{article["url"]}"""

    # send image if it exits
    if article["img"]:
        bot.send_photo(chat_id=CHAT_ID, photo=article["img"])

    # send string
    bot.send_message(chat_id=CHAT_ID,
                     text=string,
                     disable_web_page_preview=True)


def send_tradera_to_telegram(item):
    # create string
    string = f"""
Tradera
{item["title"]}
Bud:   {item["bid"]} kr - {item["bids"]} bud
Köp:   {item["buy"]} kr
Frakt: {item["shipping"]}
Tid:   {item["time"]}
Url:   {item["url"]}
"""

    # send image if it exits
    if item["img"]:
        bot.send_photo(chat_id=CHAT_ID, photo=item["img"])

    # send string
    bot.send_message(chat_id=CHAT_ID,
                     text=string,
                     disable_web_page_preview=True)
