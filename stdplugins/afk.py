"""AFK Plugin for @UniBorg
Syntax: .afk REASON"""
import asyncio
import datetime
from telethon import events
from telethon.tl import functions, types
from telethon.utils import resolve_id
from uniborg.util import admin_cmd


global USER_AFK  
global afk_time  
global last_afk_message 
global recvd_messages
USER_AFK = {}
afk_time = None
last_afk_message = {}
recvd_messages = {}


@borg.on(admin_cmd(pattern="unafk (.*)"))

async def set_not_afk(event):
    current_message = event.message.message
    await event.edit("**I'm no longer AFK**")
    if Config.COMMAND_HAND_LER + "afk" not in current_message and "yes" in USER_AFK:  # pylint:disable=E0602
        USER_AFK = {}  # pylint:disable=E0602
        afk_time = None  # pylint:disable=E0602
        # pylint:disable=E0602
        for chat_id in last_afk_message:
            await last_afk_message[chat_id].delete()
        last_afk_message = {}  # pylint:disable=E0602
        recvd_messages = "You received the following messages: \n"
        # pylint:disable=E0602
        for chat_id in recvd_messages:  # pylint:disable=E0602
            current_message = recvd_messages[chat_id]
            user_id = current_message.from_id
            message_id = current_message.id
            chat_id, _ = resolve_id(chat_id)
            if isinstance(_, types.PeerUser):
                recvd_messages += f"👉 [{chat_id}](tg://user?id={chat_id})"
                # sadly, there is no way to goto a particular message by a user,
                # after the 5.5 Android update
            else:
                recvd_messages += f"👉 https://t.me/c/{chat_id}/{message_id} \n"
        try:
            if recvd_messages != "You received the following messages: \n":
                await borg.send_message(  # pylint:disable=E0602
                    Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
                    recvd_messages,
                    link_preview=False
                )
            await borg.send_message(  # pylint:disable=E0602
                Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
                "Set AFK mode to False"
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await borg.send_message(  # pylint:disable=E0602
                event.chat_id,
                "Please set `PRIVATE_GROUP_BOT_API_ID` " + \
                "for the proper functioning of afk functionality " + \
                "in @UniBorg\n\n `{}`".format(str(e)),
                reply_to=event.message.id,
                silent=True
            )
        recvd_messages = {}


@borg.on(admin_cmd(pattern="afk (.*)"))
async def _(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if not USER_AFK:  # pylint:disable=E0602
        last_seen_status = await borg(  # pylint:disable=E0602
            functions.account.GetPrivacyRequest(
                types.InputPrivacyKeyStatusTimestamp()
            )
        )
        # logger.info(last_seen_status)
        if len(last_seen_status.rules) > 0 and isinstance(last_seen_status.rules[0], types.PrivacyValueAllowAll):
            afk_time = datetime.datetime.now()  # pylint:disable=E0602
        USER_AFK.update({"yes": reason})  # pylint:disable=E0602
        if reason:
            await event.edit("**I'm goin' AFK**")
        else:
            await event.edit("**I'm goin' AFK**")
        
        try:
            await borg.send_message(  # pylint:disable=E0602
                Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
                f"Set AFK mode to True, and Reason is {reason}"
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            logger.warn(str(e))  # pylint:disable=E0602


@borg.on(events.NewMessage(  # pylint:disable=E0602
    incoming=True,
    func=lambda e: bool(e.mentioned or e.is_private)
))
async def on_afk(event):
    if event.fwd_from:
        return
    recvd_messages[event.chat_id] = event.message
    afk_since = "**a while ago**"
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if event.chat_id in Config.UB_BLACK_LIST_CHAT:
        # don't reply if chat is added to blacklist
        return False
    if USER_AFK and not (await event.get_sender()).bot:  # pylint:disable=E0602
        reason = USER_AFK["yes"]  # pylint:disable=E0602
        if afk_time:  # pylint:disable=E0602
            now = datetime.datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "**Yesterday**"
            elif days > 1:
                if days > 6:
                    date = now + \
                        datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes)
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime("%A")
            elif hours > 1:
                afk_since = f"`{int(hours)}h{int(minutes)}m`"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m{int(seconds)}s`"
            else:
                afk_since = f"`{int(seconds)}s`"
        msg = None
        message_to_reply = f"**I'm afk right now (since {afk_since}**).\n**Reason: {reason}**" \
            if reason \
            else f"**I'm afk right now (since {afk_since})**."
        msg = await event.reply(message_to_reply)
        if event.chat_id in last_afk_message:  # pylint:disable=E0602
            last_afk_message[event.chat_id] = msg      
        
            
