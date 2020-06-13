# Ported from @TheUserge to @UniBorg by @okay_reatrd
# if you change these, you gay

"""Reply to an image/sticker/gif with .mmf` 'text on top' ; 'text on bottom
"""

import os
import time
import shlex
import logging
import textwrap
from typing import Tuple, Dict, List, Union, Optional
from PIL import Image, ImageFont, ImageDraw
import asyncio
from uniborg.util import admin_cmd, humanbytes, progress, time_formatter

_LOG = logging.getLogger(__name__)

@borg.on(admin_cmd(pattern="mmf ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    replied = event.reply_to_msg_id
    if not replied:
        await event.edit("LMAO no one's gonna help you, if u use .help now then u **Gey**")
        await borg.send_file(event.chat_id, "CAADAQADhAAD3gkwRviGxMVn5813FgQ")
            
        return
    
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    await event.edit("He he, let me use my skills")
    c_time = time.time()
    reply_message = await event.get_reply_message()
    dls = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to download")
                )
            )
    dls_loc = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, os.path.basename(dls))
    if dls.endswith(".tgs"):
        await event.edit("OMG, an Animated sticker ⊙_⊙, lemme do my bleck megik...")
        png_file = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "meme.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {dls_loc} {png_file}"
        stdout, stderr = (await runcmd(cmd))[:2]
        os.remove(dls_loc)
        if not os.path.lexists(png_file):
            await event.edit("This sticker is Gey, i won't memify it ≧ω≦")
            raise Exception(stdout + stderr)
        dls_loc = png_file
    if dls.endswith(".mp4"):
        await event.edit("Look it's GF. Oh, no it's just a Gif ")
        jpg_file = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "meme.jpg")
        await take_screen_shot(dls_loc, 0, jpg_file)
        os.remove(dls_loc)
        if not os.path.lexists(jpg_file):
            await event.edit("This Gif is Gey (｡ì _ í｡), won't memify it.")
            return
        dls_loc = jpg_file
    await event.edit("Decoration Time ≧∇≦, I'm an Artist")
    webp_file = await draw_meme_text(dls_loc, input_str)
    await borg.send_file(event.chat_id, webp_file, reply_to=event.reply_to_msg_id)
                              
    await event.delete()
    os.remove(webp_file)


async def draw_meme_text(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)
    i_width, i_height = img.size
    m_font = ImageFont.truetype("uniborg/font.ttf", int((70 / 640)*i_width))
    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ''
    draw = ImageDraw.Draw(img)
    current_h, pad = 10, 5
    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)

            draw.text(xy=(((i_width - u_width) / 2) - 1, int((current_h / 640)*i_width)),
                      text=u_text, font=m_font, fill=(0, 0, 0))
            draw.text(xy=(((i_width - u_width) / 2) + 1, int((current_h / 640)*i_width)),
                      text=u_text, font=m_font, fill=(0, 0, 0))
            draw.text(xy=((i_width - u_width) / 2, int(((current_h / 640)*i_width)) - 1),
                      text=u_text, font=m_font, fill=(0, 0, 0))
            draw.text(xy=(((i_width - u_width) / 2), int(((current_h / 640)*i_width)) + 1),
                      text=u_text, font=m_font, fill=(0, 0, 0))

            draw.text(xy=((i_width - u_width) / 2, int((current_h / 640)*i_width)),
                      text=u_text, font=m_font, fill=(255, 255, 255))
            current_h += u_height + pad
    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)

            draw.text(
                xy=(((i_width - u_width) / 2) - 1, i_height - u_height - int((20 / 640)*i_width)),
                text=l_text, font=m_font, fill=(0, 0, 0))
            draw.text(
                xy=(((i_width - u_width) / 2) + 1, i_height - u_height - int((20 / 640)*i_width)),
                text=l_text, font=m_font, fill=(0, 0, 0))
            draw.text(
                xy=((i_width - u_width) / 2, (i_height - u_height - int((20 / 640)*i_width)) - 1),
                text=l_text, font=m_font, fill=(0, 0, 0))
            draw.text(
                xy=((i_width - u_width) / 2, (i_height - u_height - int((20 / 640)*i_width)) + 1),
                text=l_text, font=m_font, fill=(0, 0, 0))

            draw.text(
                xy=((i_width - u_width) / 2, i_height - u_height - int((20 / 640)*i_width)),
                text=l_text, font=m_font, fill=(255, 255, 255))
            current_h += u_height + pad

    image_name = "memify.webp"
    webp_file = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, image_name)
    img.save(webp_file, "WebP")
    return webp_file
    
async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(*args,
                                                   stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return (stdout.decode('utf-8', 'replace').strip(),
            stderr.decode('utf-8', 'replace').strip(),
            process.returncode,
            process.pid)


async def take_screen_shot(video_file: str, duration: int, path: str = '') -> Optional[str]:
    """take a screenshot"""
    _LOG.info('[[[Extracting a frame from %s ||| Video duration => %s]]]', video_file, duration)
    ttl = duration // 2
    thumb_image_path = path or os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, f"{basename(video_file)}.jpg")
    command = f"ffmpeg -ss {ttl} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        _LOG.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None
