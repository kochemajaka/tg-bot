from aiogram.utils import executor
from config_bot import dp
from handlers import client,admin,others
from data_base import mysql_base

async def on_startup(_):            # функция,выполняющаяся при запуске бота, в данном случае запускает бд
    print("Бот вышел в инлайн")
    mysql_base.sql_start()

admin.register_handlers_admin(dp) # регистрация хендлеров из файла admin
client.register_handlers_client(dp) # регистрация хендлеров из файла client


if __name__ == '__main__':
   executor.start_polling(dp, on_startup=on_startup)        # старт эхо режима

