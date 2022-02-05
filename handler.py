
import re
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import CantRestrictChatOwner, ChatAdminRequired, UserIsAnAdministratorOfTheChat
from dispatcher import han, bot, db, cur
from aiogram import types

#
# This function adds a link to the
#
@han.message_handler(commands=["add_link", "awl"], is_admin=True)
async def LinkAdd(message: types.Message):

    links = GetLink(message)
    for link in links:
        param = cur.execute("SELECT link FROM whitelist WHERE chat_id = ? AND link = ?", (message.chat.id, link))

        if param.fetchone() is None:
            cur.execute("INSERT INTO whitelist VALUES (?, ?)", (link, message.chat.id))
            db.commit()
            await message.reply("Link added to whitelist")

        else:
            await message.reply("Link already exists")
    
#
# This function removes a link from the whitelist
#
@han.message_handler(commands=["remove_link", "rwl"], is_admin=True)
async def LinkDelete(message: types.Message):

    links = GetLink(message)
    for link in links:
        param = cur.execute("SELECT link FROM whitelist WHERE chat_id = ? AND link = ?", (message.chat.id, link))
        
        if param.fetchall() is not None:
            cur.execute("DELETE FROM whitelist WHERE chat_id = ? AND link = ?", (message.chat.id, link))
            db.commit()
            await message.reply("Link has been removed from whitelist")
        
        else:
            await message.reply("The link has already been removed from the whitelist")

#
# This function shows blocked links in the chat
#
@han.message_handler(commands=["whitelist"], is_admin=True)
async def BlackList(message: types.Message):
    linklist = ""
    
    for link in cur.execute("SELECT link FROM whitelist WHERE chat_id = ?", (message.chat.id,)):
        linklist += f"<code>{link[0]}</code>\n"
    
    await message.reply(f"Unblocked Links:\n{linklist}")

@han.message_handler()
async def wait(message:types.Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    
    if member.is_chat_admin():
        #Some code here
        pass
    
    else:
       
        for link in cur.execute("SELECT link FROM whitelist WHERE chat_id = ?", (message.chat.id,)):
            pattern = re.compile(r"(https?:\/\/)?([\w-]{1,32}\.[\w-]{1,32})[^\s@]*")
            lis = pattern.findall(message.text)
            
            for i in range(len(lis)):            
                if not (link[0] in lis[i][1]):
                    await message.delete()
                    await message.answer("Message with link deleted")
                    return
#
#
#
def GetLink(message):
    original = message.text.split(maxsplit=1)[1]
    pattern = re.compile(r"(https?:\/\/)?([\w-]{1,32}\.[\w-]{1,32})[^\s@]*")
    return pattern.findall(original)