from telethon import events
import random, re
from uniborg.util import admin_cmd
import asyncio

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats 
    "]+")

def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, '', inputString)

@borg.on(admin_cmd(pattern="waifu ?(.*)"))
async def _(event):
    """Generate random waifu sticker with the text!"""
    text = event.pattern_match.group(1)
    if not text:
        if event.is_reply:
            text = (await event.get_reply_message()).message
        else:
            await event.edit("`No text given, hence the waifu ran away.`")
            return
    animus = [20, 32, 33, 40, 41, 42, 58]
    sticcers = await event.client.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}")
    try:
        await sticcers[0].click(event.chat_id,
                                reply_to=event.reply_to_msg_id,
                                silent=True if event.is_reply else False,
                                hide_via=True)
        await event.delete()
    except IndexError:
        await event.edit("`F, can't find any waifu for you :P`")
        return
