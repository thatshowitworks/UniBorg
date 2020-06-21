# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

from asyncio import wait
from uniborg.util import admin_cmd
from telethon import events

""" .spam <n> <message>
.spamstkr <n>"""


@borg.on(events.NewMessage(pattern=r"\.spam", outgoing=True))
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        counter = int(message[6:8])
        spam_message = str(e.text[8:])

        await wait(
            [e.respond(spam_message) for i in range(counter)]
            )

        await e.delete()
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP,
                "#SPAM \n\n"
                "Spam was executed successfully"
                )

@borg.on(admin_cmd(pattern="spamstkr ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = int(event.pattern_match.group(1))
    replied = event.reply_to_msg_id
    if not replied:
    	await even.edit("Reply to a sticker you idiot.")
    	return
    reply = await event.get_reply_message()
    stickerid = reply.file.id
    await event.delete()
    for i in range(input_str):
        await event.client.send_file(event.chat_id, stickerid)
