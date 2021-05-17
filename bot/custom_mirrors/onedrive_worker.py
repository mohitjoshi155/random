import json
from base64 import b64decode
from urllib.parse import unquote

import requests
from telegram.ext import CommandHandler, run_async

from bot import Interval, LOGGER, dispatcher, DOWNLOAD_DIR, DOWNLOAD_STATUS_UPDATE_INTERVAL
from bot.modules.mirror import ariaDlManager, MirrorListener
from bot.helper.ext_utils import bot_utils
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, sendStatusMessage, update_all_messages


def get_onedrive_dl_links(url, folder=""):
    r = requests.get(url, verify=False)
    data = r.text.split("rawData = \"", 1)[1].split("\",", 1)[0]
    data = json.loads(b64decode(data))
    dl_links = []
    for each_data in data:
        new_base_folder = unquote(folder + "/" + each_data['name'])
        new_url = url + "/" + each_data['name']
        if each_data['@type'] == 'folder':
            dl_links = dl_links + get_onedrive_dl_links(new_url, new_base_folder)
        elif each_data['@type'] == 'file':
            dl_links.append({
                "folder_path": unquote(folder).encode('ascii', errors='ignore').decode(),
                "file_path": unquote(folder + "/" + each_data['name']).encode('ascii', errors='ignore').decode(),
                "file_name": unquote(each_data['name']).encode('ascii', errors='ignore').decode(),
                "url": new_url
            })

    return dl_links


@run_async
def onedrive(update, context):

    bot = context.bot
    message_args = update.message.text.split(' ')
    try:
        link = message_args[1]
    except IndexError:
        link = ''
    LOGGER.info(link)
    link = link.strip()
    tag = None
    if not bot_utils.is_url(link):
        sendMessage('No download source provided', bot, update)
        return

    root = unquote(link).rsplit("/", 1)[1].encode(errors='ignore').decode()
    if root == "":
        sendMessage('Root Error', bot, update)
        return
    links = get_onedrive_dl_links(link)

    listener = MirrorListener(bot, update, False, tag, root=root)
    ariaDlManager.add_download(f'{DOWNLOAD_DIR}/{listener.uid}/{root}/', links, listener)
    sendStatusMessage(update, bot)
    if len(Interval) == 0:
        Interval.append(bot_utils.setInterval(DOWNLOAD_STATUS_UPDATE_INTERVAL, update_all_messages))


onedrive_handler = CommandHandler("onedrive", onedrive,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
dispatcher.add_handler(onedrive_handler)
