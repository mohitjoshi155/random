import re
import binascii

from telegram.ext import CommandHandler, run_async

from bot import Interval, dispatcher, DOWNLOAD_DIR, DOWNLOAD_STATUS_UPDATE_INTERVAL
from bot.modules.mirror import MirrorListener
from bot.helper.ext_utils.bot_utils import getDownloadByGid, setInterval
from bot.helper.mirror_utils.download_utils.xdcc_download_helper import XDCCDownload
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, sendStatusMessage, update_all_messages


@run_async
def xdcc_download(update, context):

    bot = context.bot
    message_args = update.message.text.split(' ', 2)
    try:
        server_channel = message_args[1]
    except IndexError:
        server_channel = ''
    server_channel = server_channel.strip()
    if not server_channel:
        sendMessage('You need to provide a channel to join.', bot, update)
        return

    try:
        command = message_args[2]
    except IndexError:
        command = message_args[2]

    if not command:
        sendMessage('You need to provide download command.', bot, update)
        return

    server_channel = server_channel.split(",")
    server_info = {}
    args = {}

    for each_info in server_channel:
        info = each_info.split("=")
        if info[0].lower() == "channel":
            args.update({info[0]: info[1]})
        else:
            server_info.update({info[0]: info[1]})
    tag = None

    pattern = r".* (.*?) xdcc (send|batch) (.*)"
    commands = re.match(pattern, command)
    args.update({
        "bot": commands.group(1),
        "action": commands.group(2),
        "packs": commands.group(3)
    })

    gid = format(binascii.crc32((args['bot'] + args['packs']).encode('utf8')), '08x')
    if getDownloadByGid(gid):
        sendMessage('Mirror already in queue.', bot, update)
        return

    root = f"/{args['bot']} {args['packs']}/"
    listener = MirrorListener(bot, update, False, tag, root=root)
    xdcc_dl = XDCCDownload(listener)
    xdcc_dl.add_download(args, f'{DOWNLOAD_DIR}{listener.uid}/{root}')
    sendStatusMessage(update, bot)
    if len(Interval) == 0:
        Interval.append(setInterval(DOWNLOAD_STATUS_UPDATE_INTERVAL, update_all_messages))


xdcc_handler = CommandHandler("xdcc", xdcc_download,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
dispatcher.add_handler(xdcc_handler)
