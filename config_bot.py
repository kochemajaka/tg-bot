from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()   # инициализация хранилища для машины состояний

TOKEN = "1982450546:AAHlsy4LeqGdybw4cJoMdiVIAosrAcomoSo"                  # токен, выдаваемый BotFather
bot = Bot(token=TOKEN)      # присваивание токена боту
dp = Dispatcher(bot, storage=storage)       # Инициализация диспетчера


