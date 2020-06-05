"""Restrict Users
Available Commands: .ban, .unban, .mute, .unmute .tmute, .tban"""

from telethon import events
import asyncio
from datetime import datetime
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from uniborg.util import admin_cmd
from datetime import timedelta
import re
from typing import Tuple, Union


regexp = re.compile(r"(\d+)(w|d|h|m|s)?")
adminregexp = re.compile(r"\d+(?:w|d|h|m|s)?")


async def amount_to_secs(amount: tuple) -> int:

    num, unit = amount

    num = int(num)
    if not unit:
        unit = 's'

    if unit == 's':
        return num
    elif unit == 'm':
        return num * 60
    elif unit == 'h':
        return num * 60 * 60
    elif unit == 'd':
        return num * 60 * 60 * 24
    elif unit == 'w':
        return num * 60 * 60 * 24 * 7
    else:
        return 0


async def string_to_secs(string: str) -> int:
   
    values = regexp.findall(string)

    totalValues = len(values)

    if totalValues == 1:
        return await amount_to_secs(values[0])
    else:
        total = 0
        for amount in values:
            total += await amount_to_secs(amount)
        return total


async def split_extra_string(string: str) -> Tuple[
    Union[str, None], Union[int, None]
]:
    reason = string
    time = adminregexp.findall(string)
    for u in time:
        reason = reason.replace(u, '').strip()

    total_time = await string_to_secs(''.join(time))

    return reason or None, total_time or None

muted_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)
banned_rights = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)
unbanned_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None
)
unmuted_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=False,
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    embed_links=False
)
@borg.on(admin_cmd(pattern="(ban|unban) ?(.*)"))
async def _(event):
    # Space weirdness in regex required because argument is optional and other
    # commands start with ".unban"
    if event.fwd_from:
        return
    start = datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "ban":
        rights = banned_rights
    elif input_cmd == "unban":
        rights = unbanned_rights
    
    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str and "all" not in input_str:
        to_ban_id = int(input_str)
    else:
        return False
    try:
        await borg(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (Exception) as exc:
        await event.edit(str(exc))
    else:
        await event.edit(f"{input_cmd}ed Successfully")

@borg.on(admin_cmd(pattern="mute ?(.*)"))
async def _(event):
    # Space weirdness in regex required because argument is optional and other
    # commands start with ".unban"
    if event.fwd_from:
        return
    start = datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = "mute"
    if input_cmd == "ban":
        rights = 1
    elif input_cmd == "unban":
        rights = 2
    elif input_cmd == "mute":
        rights = muted_rights
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str and "all" not in input_str:
        to_ban_id = input_str
    else:
        return False
    try:
        await borg(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (Exception) as exc:
        await event.edit(str(exc))
    else:
        await event.edit(f"**Muted**")


@borg.on(admin_cmd(pattern="unmute ?(.*)"))
async def _(event):
    # Space weirdness in regex required because argument is optional and other
    # commands start with ".unban"
    if event.fwd_from:
        return
    start = datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = "unmute"
    if input_cmd == "ban":
        rights = 1
    elif input_cmd == "unban":
        rights = 2
    elif input_cmd == "unmute":
        rights = unmuted_rights
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str and "all" not in input_str:
        to_ban_id = input_str
    else:
        return False
    try:
        await borg(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (Exception) as exc:
        await event.edit(str(exc))
    else:
        await event.edit(f"**Unmuted**")


@borg.on(admin_cmd(pattern="tmute ?(.*)"))
async def _(event):
    # Space weirdness in regex required because argument is optional and other
    # commands start with ".unban"
    if event.fwd_from:
        return

    start = datetime.now()
    x = 1
    to_ban_id = None
    rights = None
    input_cmd = "tmute"
    if input_cmd == "ban":
        rights = 1
    elif input_cmd == "unban":
        rights = 2
    elif input_cmd == "tmute":
        rights = 2
    period = "time=" + event.pattern_match.group(1)
    if period == "time=":
        await event.edit("`Specify the time`")
    else:
        period = await string_to_secs(period)
        if (60 <= period < 3600):
            time = str(period//60) + " " + "minutes"
       # nit = "minutes"
        elif (3600 <= period < 86400):
            time = str(period//3600) + " " + "hours"
       # unit = "hours"
        elif period >= 86400:
            time = str(period//86400) + " " + "days"
        else:
            time = str(period) + " " + "seconds"
        if x == 1:
            reply_msg_id = event.reply_to_msg_id
            r_mesg = await event.get_reply_message()
            if not r_mesg:
                await event.edit("`Reply to a user message`")
            else:
                to_ban_id = r_mesg.from_id
                await borg(EditBannedRequest(event.chat_id, to_ban_id, ChatBannedRights(until_date=timedelta(seconds=period), view_messages=None, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)))
                await event.edit(f"**Muted for {time}**")


@borg.on(admin_cmd(pattern="tban ?(.*)"))
async def _(event):
    # Space weirdness in regex required because argument is optional and other
    # commands start with ".unban"
    if event.fwd_from:
        return

    start = datetime.now()
    x = 1
    to_ban_id = None
    rights = None
    input_cmd = "tban"
    if input_cmd == "ban":
        rights = 1
    elif input_cmd == "unban":
        rights = 2
    elif input_cmd == "tban":
        rights = 2
    period = "time=" + event.pattern_match.group(1)
    if period == "time=":
        await event.edit("`Specify the time`")
    else:
        period = await string_to_secs(period)
        if (60 <= period < 3600):
            time = str(period//60) + " " + "minutes"
       # nit = "minutes"
        elif (3600 <= period < 86400):
            time = str(period//3600) + " " + "hours"
       # unit = "hours"
        elif period >= 86400:
            time = str(period//86400) + " " + "days"
        else:
            time = str(period) + " " + "seconds"
        if x == 1:
            reply_msg_id = event.reply_to_msg_id
            r_mesg = await event.get_reply_message()
            if not r_mesg:
                await event.edit("`Reply to a user message`")
            else:
                to_ban_id = r_mesg.from_id
                await borg(EditBannedRequest(event.chat_id, to_ban_id, ChatBannedRights(until_date=timedelta(seconds=period), view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)))
                await event.edit(f"**Banned for {time}**")
