from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_markup = ReplyKeyboardMarkup(keyboard=
[
    [KeyboardButton(text="Даю согласие")]
],
resize_keyboard=True, one_time_keyboard=True)

reply_correct = ReplyKeyboardMarkup(keyboard=
[
    [KeyboardButton(text="Всё верно")],
    [KeyboardButton(text="Ввести ещё раз")]
],
resize_keyboard=True, one_time_keyboard=True)

reply_job = ReplyKeyboardMarkup(keyboard=
[
    [KeyboardButton(text="Да")],
    [KeyboardButton(text="Нет")]
],
resize_keyboard=True, one_time_keyboard=True)