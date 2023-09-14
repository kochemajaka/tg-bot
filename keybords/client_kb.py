from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
buttons1 = ["Проверить автомобиль", "Справка"]
keyboard1.add(*buttons1)

keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons2 = ["Проверить по ClinliBase", "На главную"]
b1 = KeyboardButton("Проверить по всем базам данных")
keyboard2.add(b1).row(*buttons2)
