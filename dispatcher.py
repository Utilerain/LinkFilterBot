import logging
from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher.filters import BoundFilter
import settings
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

#
#logging all events
#
bot = Bot(settings.bot_token, parse_mode='html')
han = Dispatcher(bot, storage=MemoryStorage())

root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO) 
handler = logging.FileHandler('logs.log', 'w', 'utf-8') # or whatever
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s -> %(funcName)s: %(message)s")) # or whatever
root_logger.addHandler(handler)

#
# This filter works on ONLY admins
#
class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if member.is_chat_admin():
            return True
        return False
db = sqlite3.connect("server.db")
cur = db.cursor()

han.filters_factory.bind(AdminFilter)