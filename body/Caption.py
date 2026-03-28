from pyrogram import *
from info import *
import asyncio
from Script import script
from .database import *
import re
from pyrogram.errors import FloodWait
from pyrogram.types import *

@Client.on_message(filters.command("start") & filters.private)
async def strtCap(bot, message):
    user_id = int(message.from_user.id)
    await insert(user_id)
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("➕️ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ➕️", url=f"https://t.me/CustomCaptionBot?startchannel=true")
            ],[
                InlineKeyboardButton("Hᴇʟᴘ", callback_data="help"),
                InlineKeyboardButton("Aʙᴏᴜᴛ", callback_data="about")
            ],[
                InlineKeyboardButton("🌐 Uᴘᴅᴀᴛᴇ", url=f"https://t.me/AnS_Bots"),
                InlineKeyboardButton("📜 Sᴜᴘᴘᴏʀᴛ", url=r"https://t.me/AnSBotsSupports")
        ]]
    )
    await message.reply_photo(
        photo=SILICON_PIC,
        caption=f"<b>Hᴇʟʟᴏ {message.from_user.mention}\n\nɪ ᴀᴍ ᴀᴜᴛᴏ ᴄᴀᴘᴛɪᴏɴ ʙᴏᴛ ᴡɪᴛʜ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ.\n\nFᴏʀ ᴍᴏʀᴇ ɪɴғᴏ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ᴄʟɪᴄᴋ ᴏɴ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ.\n\nMᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ »<a href='https://t.me/Silicon_Bot_Update'>Sɪʟɪᴄᴏɴ Bᴏᴛᴢ</a></b>",
        reply_markup=keyboard
    )


@Client.on_message(filters.command("channels"))
async def channels_info(client, message):
    total = await total_channels()
    active = await active_caption_channels()

    await message.reply_text(
        f"📊 **Channel Stats**\n\n"
        f"🔹 Total Connected Channels: {total}\n"
        f"🔹 Auto Caption Active: {active}"
    )

@Client.on_message(filters.private & filters.user(ADMIN)  & filters.command(["total_users"]))
async def all_db_users_here(client,message):
    silicon = await message.reply_text("Please Wait....")
    silicon_botz = await total_user()
    await silicon.edit(f"Tᴏᴛᴀʟ Usᴇʀ :- `{silicon_botz}`")

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
    if (message.reply_to_message):
        silicon = await message.reply_text("Geting All ids from database..\n Please wait")
        all_users = await getid()
        tot = await total_user()
        success = 0
        failed = 0
        deactivated = 0
        blocked = 0
        await silicon.edit(f"ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ...")
        async for user in all_users:
            try:
                time.sleep(1)
                await message.reply_to_message.copy(user['_id'])
                success += 1
            except errors.InputUserDeactivated:
                deactivated +=1
                await delete({"_id": user['_id']})
            except errors.UserIsBlocked:
                blocked +=1
                await delete({"_id": user['_id']})
            except Exception as e:
                failed += 1
                await delete({"_id": user['_id']})
                pass
            try:
                await silicon.edit(f"<u>ʙʀᴏᴀᴅᴄᴀsᴛ ᴘʀᴏᴄᴇssɪɴɢ</u>\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {tot}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")
            except FloodWait as e:
                await asyncio.sleep(t.x)
        await silicon.edit(f"<u>ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</u>\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {tot}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command("restart"))
async def restart_bot(b, m):
    silicon = await b.send_message(text="**🔄 𝙿𝚁𝙾𝙲𝙴𝚂𝚂𝙴𝚂 𝚂𝚃𝙾𝙿𝙴𝙳. 𝙱𝙾𝚃 𝙸𝚂 𝚁𝙴𝚂𝚃𝙰𝚁𝚃𝙸𝙽𝙶...**", chat_id=m.chat.id)       
    await asyncio.sleep(3)
    await silicon.edit("**✅️ 𝙱𝙾𝚃 𝙸𝚂 𝚁𝙴𝚂𝚃𝙰𝚁𝚃𝙴𝙳. 𝙽𝙾𝚆 𝚈𝙾𝚄 𝙲𝙰𝙽 𝚄𝚂𝙴 𝙼𝙴**")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.command("set_cap") & filters.channel)
async def setCap(bot, message):
    if len(message.command) < 2:
        return await message.reply(
            "Usᴀɢᴇ: **/set_cap 𝑌𝑜𝑢𝑟 𝑐𝑎𝑝𝑡𝑖𝑜𝑛 𝑈𝑠𝑒 <code>{file_name}</code> 𝑇𝑜 𝑠ℎ𝑜𝑤 𝑦𝑜𝑢𝑟 𝐹𝑖𝑙𝑒 𝑁𝑎𝑚𝑒.\n\n𝑈𝑠𝑒<code>{file_size}</code> 𝑇𝑜 𝑠ℎ𝑜𝑤 𝑦𝑜𝑢𝑟 𝐹𝑖𝑙𝑒 𝑆𝑖𝑧𝑒/n/n✓ 𝑀𝑎𝑦 𝐵𝑒 𝑁𝑜𝑤 𝑌𝑜𝑢 𝑎𝑟𝑒 𝑐𝑙𝑒𝑎𝑟💫**"
        )
    chnl_id = message.chat.id
    caption = (
        message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    )
    chkData = await chnl_ids.find_one({"chnl_id": chnl_id})
    if chkData:
        await updateCap(chnl_id, caption)
        return await message.reply(f"Your New Caption: {caption}")
    else:
        await addCap(chnl_id, caption)
        return await message.reply(f"Yᴏᴜʀ Nᴇᴡ Cᴀᴘᴛɪᴏɴ Is: {caption}")

@Client.on_message(filters.command("replace_word") & filters.channel)
async def replace_word(bot, message):
    if len(message.command) < 2:
        return await message.reply(
            "Usage: **/replace_word [original_word] [replacement_word], [original_word2] [replacement_word2]**"
        )

    chnl_id = message.chat.id
    replacements = message.text.split(" ", 1)[1]  # Get everything after /replace_word

    replacement_list = []
    for replacement_pair in replacements.split(","):
        parts = replacement_pair.strip().split(" ")
        if len(parts) < 2:
            continue  # Skip if pair is not valid
        original_word = parts[0]
        replacement_word = " ".join(parts[1:])  # Join the rest as replacement word

        replacement_list.append({"original": original_word, "replacement": replacement_word})

    await chnl_ids.update_one(
        {"chnl_id": chnl_id},
        {"$push": {"replacements": {"$each": replacement_list}}},
        upsert=True
    )
    await message.reply("**ʀᴇᴘʟᴀᴄᴇᴍᴇɴᴛ ᴡᴏʀᴅs ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇss ғᴜʟʟʏ.** ✅")

@Client.on_message(filters.command("del_replace_words") & filters.channel)
async def del_replace_words(bot, message):
    chnl_id = message.chat.id
    channel_data = await chnl_ids.find_one({"chnl_id": chnl_id})
    if channel_data and "replacements" in channel_data:
        await chnl_ids.update_one({"chnl_id": chnl_id}, {"$unset": {"replacements": ""}})
        await message.reply("**ᴀʟʟ ʀᴇᴘʟᴀᴄᴇᴍᴇɴᴛ ᴡᴏʀᴅs ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ.**")
    else:
        await message.reply("**ɴᴏ ʀᴇᴘʟᴀᴄᴇᴍᴇɴᴛ ᴡᴏʀᴅs ғᴏᴜɴᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ.**")


@Client.on_message(filters.command("rem_words") & filters.channel)
async def setRemWords(bot, message):
    if len(message.command) < 2:
        return await message.reply(
            "Usage: **/rem_words word1 word2** - ᴀᴅᴅ ᴡᴏʀᴅs ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʀᴇᴍᴏᴠᴇ ғʀᴏᴍ ғɪʟᴇ ɴᴀᴍᴇ"
        )
    chnl_id = message.chat.id
    words = message.command[1:] 
    await addRemWords(chnl_id, words)
    await message.reply(f"Added words to remove: {', '.join(words)}")

@Client.on_message(filters.command("del_rem_words") & filters.channel)
async def delRemWords(bot, message):
    chnl_id = message.chat.id

    channel_data = await chnl_ids.find_one({"chnl_id": chnl_id})
    if channel_data and "rem_words" in channel_data:
        await chnl_ids.update_one({"chnl_id": chnl_id}, {"$unset": {"rem_words": ""}})
        await message.reply("**ᴀʟʟ ʀᴇᴍᴏᴠᴇ ᴡᴏʀᴅs ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ.**")
    else:
        await message.reply("**ɴᴏ ʀᴇᴍᴏᴠᴇ ᴡᴏʀᴅs ғᴏᴜɴᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ.**")

@Client.on_message(filters.command("del_cap") & filters.channel)
async def delCap(_, msg):
    chnl_id = msg.chat.id
    try:
        await chnl_ids.delete_one({"chnl_id": chnl_id})
        return await msg.reply("<b><i>✓ Sᴜᴄᴄᴇssғᴜʟʟʏ... Dᴇʟᴇᴛᴇᴅ Yᴏᴜʀ Cᴀᴘᴛɪᴏɴ Nᴏᴡ I ᴀᴍ Usɪɴɢ Mʏ Dᴇғᴀᴜʟᴛ Cᴀᴘᴛɪᴏɴ </i></b>")
    except Exception as e:
        e_val = await msg.replay(f"ERR I GOT: {e}")
        await asyncio.sleep(5)
        await e_val.delete()
        return

def extract_language(default_caption):
    language_pattern = r'\b(Hindi|English|Tamil|Telugu|Malayalam|Kannada|Hin)\b'#Contribute More Language If You Have
    languages = set(re.findall(language_pattern, default_caption, re.IGNORECASE))
    if not languages:
        return "Hindi-English"
    return ", ".join(sorted(languages, key=str.lower))

def extract_year(default_caption):
    match = re.search(r'\b(19\d{2}|20\d{2})\b', default_caption)
    return match.group(1) if match else None

def apply_word_replacements(file_name, replacements):
    for item in replacements:
        original = item["original"]
        replacement = item["replacement"]
        file_name = re.sub(rf"\b{re.escape(original)}\b", replacement, file_name, flags=re.IGNORECASE)
    return file_name

def format_duration(duration):
    if duration:
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60
        formatted_duration = ""

        if hours > 0:
            formatted_duration += f"{hours}H-"
        if minutes > 0:
            formatted_duration += f"{minutes}M-"

        formatted_duration += f"{seconds:02}Sec"
        return formatted_duration
    return "N/A"

@Client.on_message(filters.channel)
async def reCap(bot, message):
    chnl_id = message.chat.id
    default_caption = message.caption
    if message.media:
        for file_type in ("video", "audio", "document", "voice"):
            obj = getattr(message, file_type, None)
            if obj and hasattr(obj, "file_name"):
                file_name = obj.file_name
                file_size = obj.file_size
                language = extract_language(default_caption)
                year = extract_year(default_caption)
                duration = formatted_duration,
                height = height or "N/A", 
                width=width or "N/A",
                file_name = (
                    re.sub(r"@\w+\s*", "", file_name)
                    .replace("_", " ")
                    .replace(".", " ")
                )
                replacements = await get_replacements(chnl_id)
                file_name = apply_word_replacements(file_name, replacements)

                rem_words = await getRemWords(chnl_id)
                for word in rem_words:
                    file_name = re.sub(rf"\b{re.escape(word)}\b", "", file_name)
                cap_dets = await chnl_ids.find_one({"chnl_id": chnl_id})
                try:
                    if cap_dets:
                        cap = cap_dets["caption"]
                        replaced_caption = cap.format(file_name=file_name, file_size=get_size(file_size), default_caption=default_caption, language=language, year=year)
                        await message.edit(replaced_caption)
                    else:
                        replaced_caption = DEF_CAP.format(file_name=file_name, file_size=get_size(file_size), default_caption=default_caption, language=language, year=year, duration = formatted_duration, height = height or "N/A", width = width or "N/A",)
                        await message.edit(replaced_caption)
                except FloodWait as e:
                    await asyncio.sleep(e)
                    continue
    return

# Size conversion function
def get_size(size):
    units = ["Bytes", "Kʙ", "Mʙ", "Gʙ", "Tʙ", "Pʙ", "Eʙ"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units) - 1:  # Changed the condition to stop at the last unit
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

@Client.on_callback_query(filters.regex(r'^start'))
async def start(bot, query):
    await query.message.edit_text(
        text=script.START_TXT.format(query.from_user.mention),  
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("➕️ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ➕️", url=f"http://t.me/CustomCaptionBot?startchannel=true")
                ],[
                InlineKeyboardButton("Hᴇʟᴘ", callback_data="help"),
                InlineKeyboardButton("Aʙᴏᴜᴛ", callback_data="about")
            ],[
                InlineKeyboardButton("🌐 Uᴘᴅᴀᴛᴇ", url=f"https://t.me/AnS_Bots"),
                InlineKeyboardButton("📜 Sᴜᴘᴘᴏʀᴛ", url=r"https://t.me/AnSBotsSupports")
            ]]
        ),
        disable_web_page_preview=True
)

@Client.on_callback_query(filters.regex(r'^help'))
async def help(bot, query):
    await query.message.edit_text(
        text=script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton('About', callback_data='about')
            ],[
            InlineKeyboardButton('↩ ʙᴀᴄᴋ', callback_data='start')
            ]]
        ),
        disable_web_page_preview=True    
)


@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query):
    await query.message.edit_text(
        text=script.ABOUT_TXT,
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton('ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ❓', callback_data='help')
            ],[
            InlineKeyboardButton('↩ ʙᴀᴄᴋ', callback_data='start')
            ]]
        ),
        disable_web_page_preview=True 

)

