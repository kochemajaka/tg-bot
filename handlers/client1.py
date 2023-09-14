=
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor



TOKEN = "1982450546:AAHlsy4LeqGdybw4cJoMdiVIAosrAcomoSo"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


import requests

# @dp.message_handler(content_types=['photo'])
# async def cmd_create_dem(message: types.Message):
#         st1r = str(len(message.photo))
#         with open('example.txt', 'a') as f:
#                 f.write(st1r)
#
# @dp.message_handler(commands=['dem'])
# @dp.message_handler(content_types=['photo'])
# async def cmd_create_dem(message: types.Message):
#     file_info = await bot.get_file(message.photo[-1].file_id)
#     downloaded_file = (await bot.download_file(file_info.file_path)).read()
#     src = r'C:/Users/Семен/Desktop/photo' + message.photo[0].file_id
#     with open(src, 'wb') as new_file:
#         new_file.write(downloaded_file)
#     await message.answer("Фото успешно скачано!")

# @dp.message_handler(content_types=['photo'])
# async def download_file(message: types.Message):
#     file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
#     destination = r"C:/Users/Семен/Desktop/photo"
#     await bot.download_file(file_info.file_path, destination)
#     await message.answer("Фото успешно скачано!")

@dp.message_handler(content_types=['photo'])
async def cmd_create_dem(message: types.Message):
    for i in range(2):
        await message.photo[-1].download(destination_file=fr"C:/Users/Семен/Desktop/photo/test_{i}.jpg")
    await message.answer("Фото успешно скачано!")

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)




#
#
#
# from config_bot import dp
# from aiogram import types
# from keybords import keyboard1,keyboard2
# import aiogram.utils.markdown as fmt
# from handlers import check_vin
# from data_base import mysql_base
#
#
#
# VIN = ""
# flag = ""
#
# async def process_start_command(message: types.Message):
#     await message.reply("Бот по проверке авто по VIN номеру, приветствует вас!", reply_markup=keyboard1)
#
# async def process_help_command(message: types.Message):
#     await message.reply(fmt.text(
#             fmt.text("Cервис, предоставляющий полный и правдивый отчет по истории владения и эксплуатации автомобилей, \
#                     зарегистрированных на территории РФ."),
#             fmt.text("Проверка осуществляется по VIN, номеру шасси или государственному регистрационному знаку (номеру)."),
#             fmt.text("Для получения информации об автомобиле:"),
#             fmt.text("  - нажмите на кнопку «Проверить автомобиль»"),
#             fmt.text("  - отправьте боту сообщение с номером автомобиля"),
#             fmt.text("  -ответным сообщением вы получите отчет об автомобиле"),
#             sep="\n"
#         ), parse_mode="HTML", reply_markup=keyboard2)
#
# async def get_text_messages(msg: types.Message):
#     message = msg.text
#     message = message.lower()
#     global flag
#     global vin
#     match message:
#         case "проверить автомобиль":
#             await msg.reply("Выберите, что бы вы хотели проверить:", reply_markup=keyboard2)
#
#         case "проверить по clinlibase":
#             if vin!="":
#                 await msg.answer(f"Отчет ClinliBase по номеру: {vin}")
#                 await mysql_base.sql_read_command(vin, msg.from_user.id)
#                 vin = ""
#                 flag = ""
#             else:
#                 flag = "clinli"
#                 await msg.reply("Введите VIN код в формате FALP62W4WH1287053 или гос.номер в формате: А001МР77")
#
#         case "проверить по всем базам данных":
#             if vin!="":
#                 await msg.answer(f"Отчет всех баз по номеру: {vin}")
#                 await mysql_base.sql_read_command(vin, msg.from_user.id)
#                 vin = ""
#                 flag = ""
#             else:
#                 flag = "all"
#                 await msg.reply("Введите VIN код в формате FALP62W4WH1287035 или гос.номер в формате: А001МР77")
#
#         case "на главную":
#             await msg.reply("Бот по проверке авто по VIN номеру, приветствует вас!", reply_markup=keyboard1)
#
#         case "справка":
#             await msg.reply(fmt.text(
#                 fmt.text("Cервис, предоставляющий полный и правдивый отчет по истории владения и эксплуатации автомобилей, \
#                                 зарегистрированных на территории РФ."),
#                 fmt.text(
#                     "Проверка осуществляется по VIN, номеру шасси или государственному регистрационному знаку (номеру)."),
#                 fmt.text("Для получения информации об автомобиле:"),
#                 fmt.text("  - нажмите на кнопку «Проверить автомобиль»"),
#                 fmt.text("  - отправьте боту сообщение с номером автомобиля"),
#                 fmt.text("  -ответным сообщением вы получите отчет об автомобиле"),
#                 sep="\n"
#             ), parse_mode="HTML", reply_markup=keyboard2)
#
#         case _:
#             message = message.upper()
#             if check_vin.IF_VIN(message):
#                 vin = check_vin.IF_VIN(message)
#             else: vin=""
#             if vin!="":
#                 match flag:
#                     case "clinli":
#                         await msg.answer(f"Отчет ClinliBase по номеру: {vin}")
#                         await mysql_base.sql_read_command(vin,msg.from_user.id)
#                         vin = ""
#                         flag = ""
#
#                     case "all":
#                         #запрос к бд
#                         await msg.answer(f"Отчет всех баз по номеру: {vin}")
#                         await mysql_base.sql_read_command(vin, msg.from_user.id)
#                         vin = ""
#                         flag = ""
#                     case _:
#                         await msg.answer("Выберите, что бы вы хотели проверить:", reply_markup=keyboard2)
#             else:
#                 await msg.answer("Извините, ваше сообщение не распознано, либо VIN введен не корректно", reply_markup=keyboard2)
#                 await msg.delete()
#
#
#
#
#
# def register_handlers_client(dp: dp):
#     dp.register_message_handler(process_start_command, commands=['start'])
#     dp.register_message_handler(process_help_command, commands=['help'])
#     dp.register_message_handler(get_text_messages)

# async def get_text_messages(msg: types.Message):
#     message = msg.text
#     message = message.lower()
#     global vin
#     match message:
#         case "проверить автомобиль":
#             await msg.reply("Выберите, что бы вы хотели проверить:", reply_markup=keyboard2)
#
#         case "проверить по clinlibase":
#             if vin!="":
#                 await msg.answer(f"Отчет ClinliBase по номеру: {vin}")
#                 await mysql_base.sql_read_command(vin, msg.from_user.id)
#             else:
#                 await msg.reply("Введите VIN код в формате FALP62W4WH1287053 или гос.номер в формате: А001МР77")
#
#         case "проверить по всем базам данных":
#             if vin!="":
#                 await msg.answer(f"Отчет всех баз по номеру: {vin}")
#                 await mysql_base.sql_read_command(vin, msg.from_user.id)
#             else:
#                 await msg.reply("Введите VIN код в формате FALP62W4WH1287035 или гос.номер в формате: А001МР77")
#
#         case "на главную":
#             await msg.reply("Бот по проверке авто по VIN номеру, приветствует вас!", reply_markup=keyboard1)
#
#         case "справка":
#             await msg.reply(fmt.text(
#                 fmt.text("Cервис, предоставляющий полный и правдивый отчет по истории владения и эксплуатации автомобилей, \
#                                 зарегистрированных на территории РФ."),
#                 fmt.text(
#                     "Проверка осуществляется по VIN, номеру шасси или государственному регистрационному знаку (номеру)."),
#                 fmt.text("Для получения информации об автомобиле:"),
#                 fmt.text("  - нажмите на кнопку «Проверить автомобиль»"),
#                 fmt.text("  - отправьте боту сообщение с номером автомобиля"),
#                 fmt.text("  -ответным сообщением вы получите отчет об автомобиле"),
#                 sep="\n"
#             ), parse_mode="HTML", reply_markup=keyboard2)
#
#         case _:
#             message = message.upper()
#             if check_vin.IF_VIN(message):
#                 vin = check_vin.IF_VIN(message)
#             else:
#                 await msg.answer("Извините, ваше сообщение не распознано, либо VIN введен не корректно", reply_markup=keyboard2)
#                 await msg.delete()