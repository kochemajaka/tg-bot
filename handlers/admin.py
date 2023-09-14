from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from config_bot import dp
from aiogram.dispatcher.filters import Text
from data_base import mysql_base
from handlers import check_vin

ID = None
count = 0

class FSMAdmin(StatesGroup):  # State machine
    VIN = State()
    trademark = State()
    year = State()
    odometer = State()
    description = State()
    cnt_foto = State()



# @dp.message_handler(commands='upload', state=None, is_chat_admin=True)  # Подключаем машину состояний
async def cm_start(message: types.Message):
    global ID
    ID = message.from_user.id
    await message.answer("Введи VIN")
    await FSMAdmin.VIN.set()


# @dp.message_handler(state=FSMAdmin.VIN)            #Ловим ВИН номер
async def load_VIN(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        if check_vin.IF_VIN(message.text):
            async with state.proxy() as data:
                data['VIN'] = message.text
            await FSMAdmin.next()
            await message.reply("Введи марку/модель автомобиля")
        else:
            await message.reply("VIN указан некорректно.")

# Выход из состояний
# @dp.message_handler(state="*", commands="cancel")
# @dp.message_handler(Text(equals="cancel",ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
        curren_state = await state.get_state()
        if curren_state is None:
            return
        await state.finish()
        await message.reply("Запись в базу данных прекращена")
        

# @dp.message_handler(state=FSMAdmin.trademark)            Ловим марку/модель
async def load_trademark(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['trademark'] = message.text
        await FSMAdmin.next()
        await message.reply("Введи год выпуска автомобиля")


# @dp.message_handler(state=FSMAdmin.year)            Ловим год автомобиля
async def load_year(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['year'] = message.text
        await FSMAdmin.next()
        await message.reply("Введи пробег автомобиля")


# @dp.message_handler(state=FSMAdmin.odometer)            Ловим пробег
async def load_odometer(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['odometer'] = message.text
        await FSMAdmin.next()
        await message.reply("Введи описание автомобиля")


# @dp.message_handler(state=FSMAdmin.description)            Ловим описание
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply("Введите количество фотографий автомобиля")


# @dp.message_handler(state=FSMAdmin.cnt_foto)            Ловим описание
async def load_cnt_foto(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        global count
        count = 0
        if (message.text in ["1","2","3","4","5","6","7","8","9","10"]):
            async with state.proxy() as data:
                data['cnt_foto'] = int(message.text)
            await FSMAdmin.next()
            await message.reply(f"Загрузи {message.text} фото автомобиля")
            await mysql_base.sql_add_command(state, message.chat.id)
        else:
            await message.reply("Количество фото указанно неверно(от 1 до 10).")

# @dp.message_handler(content_types=['photo'], state = FSMAdmin.file)            Загружаем фото
async def load_file(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            VIN = data['VIN']
        await message.photo[-1].download(destination_file=fr"C:/Users/Семен/Desktop/photo/{VIN}_{count}.jpg")
        count += 1
        await state.finish()



def register_handlers_admin(dp : Dispatcher):           # регистрация хендлеров
    dp.register_message_handler(cm_start, commands=['upload'], is_chat_admin=True)
    dp.register_message_handler(cancel_handler, commands=['cancel'], state="*")
    dp.register_message_handler(cancel_handler, Text(equals="cancel",ignore_case=True), state="*")
    dp.register_message_handler(load_VIN, state=FSMAdmin.VIN)
    dp.register_message_handler(load_trademark, state=FSMAdmin.trademark)
    dp.register_message_handler(load_year, state=FSMAdmin.year)
    dp.register_message_handler(load_odometer, state=FSMAdmin.odometer)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_cnt_foto, state=FSMAdmin.cnt_foto)
    dp.register_message_handler(load_file, content_types=['photo'])


