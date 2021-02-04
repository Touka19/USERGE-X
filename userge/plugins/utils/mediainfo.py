"""MEDIA INFO"""

# Suggested by - @d0n0t (https://github.com/code-rgb/USERGE-X/issues/9)
# Copyright (C) 2020 BY - GitHub.com/code-rgb [TG - @deleteduser420]
# All rights reserved.

import os

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from userge import Message, userge
from userge.utils import post_to_telegraph, runcmd, safe_filename


@userge.on_cmd("mediainfo", about={"header": "Get Detailed Info About Replied Media"})
async def mediainfo(message: Message):
    """Get Media Info"""
    reply = message.reply_to_message
    if not reply:
        await message.err("reply to media first", del_in=5)
        return
    process = await message.edit("`Processing ...`")
    x_media = None
    available_media = ("audio", "document", "photo", "sticker", "animation", "video", "voice", "video_note",
                        "new_chat_photo")
    for kind in available_media:
        x_media = getattr(reply, kind, None)
        if x_media is not None:
            break
    if x_media is None:
        await message.err("Reply To a Vaild Media Format", del_in=3)
        return
    media_type = str(type(x_media)).split("'")[1]
    file_path = safe_filename(await reply.download())
    output_ = await runcmd(f"mediainfo {file_path)}")
    out = output_[0] if len(output_) != 0 else "Not Supported"
    body_text = f"""
<h2>Json</h2>
<pre>{x_media}</pre>
<br>

<h2>Details</h2>
<pre>{out}</pre>
"""
    link = post_to_telegraph(media_type, body_text)
    if message.client.is_bot:
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=x_media.upper(), url=link)]]
        )
        await process.edit_text("ℹ️  <b>MEDIA INFO</b>", reply_markup=markup)
    else:
        await message.edit(f"ℹ️  <b>MEDIA INFO:  [{x_media.upper()}]({link})</b>")
    os.remove(file_path)