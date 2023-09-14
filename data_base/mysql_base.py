import sqlite3 as sq
from config_bot import bot
from config_bot import dp
from aiogram import types

def sql_start():        # создание или подключение базы данных
    global base,cur
    base = sq.connect(f"data_base/car.bd")
    cur = base.cursor()
    if base:
        print("База данных успешно подключена!")
    base.execute('CREATE TABLE IF NOT EXISTS car(VIN TEXT PRIMARY KEY, trademark TEXT, year TEXT, odometer TEXT, description TEXT, photo INTEGER)')
    base.commit()

async def sql_add_command(state,ID): # функция для добавления информации в бд
    async with state.proxy() as data:
        cur.execute("INSERT INTO car VALUES (?,?,?,?,?,?)",tuple(data.values()))
        base.commit()
        await bot.send_message(ID, "Данные успешно загружены.")

def sql_read_command(VIN):   # функция для чтения информации из бд
    data = cur.execute('SELECT * FROM car WHERE VIN == ?',(VIN,)).fetchone()
    # await bot.send_message(ID, f'Марка/модель: {data[1]}\n Год выпуска: {data[2]} \nПробег: {data[3]} \nОписание: {data[4]}')
    # media = types.MediaGroup()
    # for i in range (int(data[5])):
    #     media.attach_photo(types.InputFile(fr"C:/Users/Семен/Desktop/photo/{data[0]}_{i}.jpg","rb"))
    # await bot.send_media_group(ID, media=media)
    input_data = [data[0],data[1],data[2],data[3],data[4]]
    return (input_data)

def sql_find_command(VIN):  # проверка на наличие информации в базе данных
    data = cur.execute('SELECT * FROM car WHERE VIN == ?',(VIN,)).fetchone()
    if data!=None:
        return True
    else:
        return False