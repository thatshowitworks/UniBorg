import asyncio
from telethon import events
from telethon import version
from platform import python_version, uname
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd

DEFAULTUSER = Config.ALIVE_NAME
Alive = Config.CUSTOM_ALIVE

@borg.on(admin_cmd("alive"))
async def _(event):
    if event.fwd_from:
        return
    if Alive:
       mentions = f"{Alive}.\n\nTelethon version: {version.__version__}.\nPython: {python_version()}.\nUser: {DEFAULTUSER}."
    else:
       mentions = f"My bot is running.\n\nTelethon version: {version.__version__}.\nPython: {python_version()}.\nUser: {DEFAULTUSER}."
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()                   
