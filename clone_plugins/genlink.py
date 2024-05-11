import re
import base64
from pyrogram import filters, Client, enums
from plugins.database import unpack_new_file_id
from clone_plugins.users_api import get_user, get_short_link

@Client.on_message(filters.command(['link', 'plink', 'batch']))
async def gen_link_s(client: Client, message):
    replied = message.reply_to_message
    if not replied:
        return await message.reply('Reply to a message to get a shareable link.')
    
    file_type = replied.media
    if file_type not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
        return await message.reply("Reply to a supported media")
    
    if message.has_protected_content:
        return await message.reply("okDa")
    
    file_id, ref = unpack_new_file_id((getattr(replied, file_type.value)).file_id)
    string = 'filep_' if message.text.lower().strip() == "/plink" else 'file_'
    string += file_id
    outstr = base64.urlsafe_b64encode(string.encode("ascii")).decode().strip("=")
    user_id = message.from_user.id
    user = await get_user(user_id)
    
    # Generate individual share links
    bot_username = (await client.get_me()).username
    share_link = f"https://t.me/{bot_username}?start={outstr}"
    short_link = await get_short_link(user, share_link)
    
    # Handle batch command
    if message.command[0] == 'batch':
        # Generate batch link
        batch_link = f"https://t.me/{bot_username}?start=batch_{outstr}"
        batch_short_link = await get_short_link(user, batch_link)
        await message.reply(f"<b>Batch Link:\n{batch_short_link}</b>")
    else:
        # Reply with individual share link
        await message.reply(f"<b>Original Link:\n{share_link}</b>")
        await message.reply(f"<b>Short Link:\n{short_link}</b>")
