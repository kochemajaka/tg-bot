from config_bot import dp
from aiogram import types
from keybords import keyboard1,keyboard2
import aiogram.utils.markdown as fmt
from handlers import check_vin
from data_base import mysql_base
from parsing import report_maker
from config_bot import bot

vin = ""
flag = ""

async def process_start_command(message: types.Message): # обработка комманды /start
    await message.reply("Бот по проверке авто по VIN номеру, приветствует вас!", reply_markup=keyboard1)

async def process_help_command(message: types.Message):   # обработка комманды /help
    await message.reply(fmt.text(
            fmt.text("Cервис, предоставляющий полный и правдивый отчет по истории владения и эксплуатации автомобилей, \
                    зарегистрированных на территории РФ."),
            fmt.text("Проверка осуществляется по VIN, номеру шасси или государственному регистрационному знаку (номеру)."),
            fmt.text("Для получения информации об автомобиле:"),
            fmt.text("  - нажмите на кнопку «Проверить автомобиль»"),
            fmt.text("  - отправьте боту сообщение с номером автомобиля"),
            fmt.text("  -ответным сообщением вы получите отчет об автомобиле"),
            sep="\n"
        ), parse_mode="HTML", reply_markup=keyboard2)

async def get_text_messages(msg: types.Message): # обработка остальных сообщений
    message = msg.text
    message = message.lower()
    global flag
    global vin
    match message:  #определние типа сообщения
        case "проверить автомобиль":
            await msg.reply("Выберите, что бы вы хотели проверить:", reply_markup=keyboard2)

        case "проверить по clinlibase":
            if vin != "":
                if mysql_base.sql_find_command(vin):
                    await msg.answer(f"Отчет ClinliBase по номеру: {vin}")
                    base = mysql_base.sql_read_command(vin)
                    report_maker.make_report(vin, base)
                    await bot.send_document(msg.from_user.id,open(fr"C:/Users/Семен/Desktop/питон/тг бот/{vin}.pdf", "rb"))

                else:
                    await msg.reply("Извините, данное авто отсутствует в базе данных.")
                vin = ""
                flag = ""
            else:
                flag = "clinli"
                await msg.reply("Введите VIN код в формате FALP62W4WH1287053 или гос.номер в формате: А001МР77")

        case "проверить по всем базам данных":
            if vin!="":
                if mysql_base.sql_find_command(vin):
                    await msg.answer(f"Отчет всех баз по номеру: {vin}")
                    base = mysql_base.sql_read_command(vin)
                    report_maker.make_report(vin, base, True)
                    await bot.send_document(msg.from_user.id,open(fr"C:/Users/Семен/Desktop/питон/тг бот/{vin}.pdf", "rb"))
                    await bot.send_document(msg.from_user.id,open(fr"C:/Users/Семен/Desktop/питон/тг бот/{vin}.pdf", "rb"))
                else:
                    await msg.reply("Извините, данное авто отсутствует в базе данных.")
                vin = ""
                flag = ""
            else:
                flag = "all"
                await msg.reply("Введите VIN код в формате FALP62W4WH1287035 или гос.номер в формате: А001МР77")

        case "на главную":
            await msg.reply("Бот по проверке авто по VIN номеру, приветствует вас!", reply_markup=keyboard1)

        case "справка":
            await msg.reply(fmt.text(
                fmt.text("Cервис, предоставляющий полный и правдивый отчет по истории владения и эксплуатации автомобилей, \
                                зарегистрированных на территории РФ."),
                fmt.text(
                    "Проверка осуществляется по VIN, номеру шасси или государственному регистрационному знаку (номеру)."),
                fmt.text("Для получения информации об автомобиле:"),
                fmt.text("  - нажмите на кнопку «Проверить автомобиль»"),
                fmt.text("  - отправьте боту сообщение с номером автомобиля"),
                fmt.text("  -ответным сообщением вы получите отчет об автомобиле"),
                sep="\n"
            ), parse_mode="HTML", reply_markup=keyboard2)

        case _:
            message = message.upper()
            if check_vin.IF_VIN(message):
                vin = check_vin.IF_VIN(message)
            else: vin=""
            if vin!="":
                match flag:
                    case "clinli":
                        if mysql_base.sql_find_command(vin):
                            await msg.answer(f"Отчет всех баз по номеру: {vin}")
                            base = mysql_base.sql_read_command(vin)
                            report_maker.make_report(vin, base)
                            await bot.send_document(msg.from_user.id, open(fr"C:/Users/Семен/Desktop/питон/тг бот/{vin}.pdf", "rb"))
                        else:
                            await msg.reply("Извините, данное авто отсутствует в базе данных.")
                        vin = ""
                        flag = ""

                    case "all":
                        if mysql_base.sql_find_command(vin):
                            await msg.answer(f"Отчет всех баз по номеру: {vin}")
                            base = mysql_base.sql_read_command(vin)
                            report_maker.make_report(vin, base,True)
                            await bot.send_document(msg.from_user.id,open(fr"C:/Users/Семен/Desktop/питон/тг бот/{vin}.pdf", "rb"))
                        else:
                            await msg.reply("Извините, данное авто отсутствует в базе данных.")
                        vin = ""
                        flag = ""
                    case _:
                        await msg.answer("Выберите, что бы вы хотели проверить:", reply_markup=keyboard2)
            else:
                await msg.answer("Извините, ваше сообщение не распознано, либо VIN введен не корректно", reply_markup=keyboard2)
                await msg.delete()





def register_handlers_client(dp: dp):  # регистрация хендлеров
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(process_help_command, commands=['help'])
    dp.register_message_handler(get_text_messages)