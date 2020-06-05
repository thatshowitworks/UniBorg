"""@RollADie
Syntax: .dice, .dart, .ball"""

from telethon.tl.types import InputMediaDice
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="dice ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🎲"))
    if input_str:
        try:
            required_number = int(input_str)
            if required_number >=7:
                  required_number = 6
            if required_number <=0:
                  required_number = 1
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🎲"))
        except:
            pass



@borg.on(admin_cmd(pattern="dart ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🎯"))
    if input_str:
        try:
            required_number = int(input_str)
            if required_number >=7:
                  required_number = 6
            if required_number <=0:
                  required_number = 1
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🎯"))
        except:
            pass


@borg.on(admin_cmd(pattern="ball ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🏀"))
    if input_str:
        try:
            required_number = int(input_str)
            if required_number >=6:
                  required_number = 5
            if required_number <=0:
                  required_number = 1
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🏀"))
        except:
            pass
