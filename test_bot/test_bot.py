from aiogram.utils import executor
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as fmt
from handlers import check_vin
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove


keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
buttons1 = KeyboardButton("Проверить по всем базам данных")
buttons2 = KeyboardButton("Проверить по ClinliBase")
keyboard1.row(buttons1).row(buttons2)

keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons2 = ["Проверить по ClinliBase", "Справка"]
b1 = KeyboardButton("Проверить по всем базам данных")
keyboard2.add(b1).row(*buttons2)

TOKEN = "1982450546:AAHlsy4LeqGdybw4cJoMdiVIAosrAcomoSo"

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

class FSMAdmin(StatesGroup):
    VIN = State()
    type_report= State()

async def on_startup(_):
    print("Бот вышел в инлайн")

@dp.message_handler(commands='start', state=None)
async def process_start_command(message: types.Message, state: FSMContext):
    await message.reply("Бот по проверке авто по VIN номеру, приветствует вас!", reply_markup=keyboard2)
    await FSMAdmin.type_report.set()


@dp.message_handler(state=FSMAdmin.type_report)
async def set_state1(state: FSMContext):
    async with state.proxy() as data:
        data['type_report'] = ""
    await FSMAdmin.next()

@dp.message_handler(state=FSMAdmin.VIN)
async def set_state2(state: FSMContext):
    async with state.proxy() as data:
        data['VIN'] = ""

@dp.message_handler(commands='help')
async def process_help_command(message: types.Message):
    await message.reply(fmt.text(
            fmt.text("Cервис, предоставляющий полный и правдивый отчет по истории владения и эксплуатации автомобилей, \
                    зарегистрированных на территории РФ."),
            fmt.text("Проверка осуществляется по VIN, номеру шасси или государственному регистрационному знаку (номеру)."),
            fmt.text("Для получения информации об автомобиле:"),
            fmt.text("  - нажмите на кнопку «Проверить автомобиль»"),
            fmt.text("  - отправьте боту сообщение с номером автомобиля"),
            fmt.text("  -ответным сообщением вы получите отчет об автомобиле"),
            sep="\n"
        ), parse_mode="HTML", reply_markup=keyboard1)


@dp.message_handler(state=FSMAdmin.type_report)
async def set_report(msg: types.Message, state: FSMContext):
    message = msg.text
    message = message.lower()
    match message:
        case "проверить по всем базам данных":
            await msg.reply("Введите VIN код в формате FALP62W4WH1287053 или гос.номер в формате: А001МР77")
            async with state.proxy() as data:
                data['type_report'] = "all"
            await FSMAdmin.next()
        case "проверить по clinlibase":
            await msg.reply("Введите VIN код в формате FALP62W4WH1287053 или гос.номер в формате: А001МР77")
            async with state.proxy() as data:
                data['type_report'] = "clinli"
            await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.VIN)
async def set_VIN(msg: types.Message, state: FSMContext):
    mesage = message.text.upper()
    async with state.proxy() as data:
        type_report = data['type_report']
        VIN = data['VIN']
    if type_report != '' and VIN!='':
        match type_report:
            case "проверить по clinlibase":
                # запрос к бд
                await msg.answer(f"Отчет ClinliBase по номеру: {VIN}")
            case "проверить по всем базам данных":
                # запрос к бд
                await msg.answer(f"Отчет всех баз по номеру: {VIN}")
    elif type_report != '' and VIN=='':
        await msg.reply("Введите VIN код в формате FALP62W4WH1287053 или гос.номер в формате: А001МР77")
    elif type_report == '' and VIN!='':
        await msg.reply("Выберите тип отчета", reply_markup=keyboard1)
    else:
        vin = check_vin.IF_VIN(mesage)
        if vin:
            async with state.proxy() as data:
                 data['VIN'] = vin
        else:
            await msg.reply("Ваше сообщение не распознано",reply_markup=keyboard2)



if __name__ == '__main__':
   executor.start_polling(dp, on_startup=on_startup)

# case
# _:
# message = message.upper()
# async with state.proxy() as data:
#     type_report = data['type_report']
# if check_vin.IF_VIN(message) and type_report != '':
#     match type_report:
#         case "проверить по clinlibase":
#             # запрос к бд
#             await msg.answer(f"Отчет ClinliBase по номеру: {message}")
#
#         case "проверить по всем базам данных":
#             # запрос к бд
#             await msg.answer(f"Отчет всех баз по номеру: {message}")
# else:
#     async with state.proxy() as data:
#         data["VIN"] = message.text
#     await FSMAdmin.next()