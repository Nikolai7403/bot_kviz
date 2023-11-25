from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="А)",callback_data="А)")
    keyboard_builder.button(text="Б)",callback_data="Б)")
    keyboard_builder.button(text="В)",callback_data="В)")
    keyboard_builder.button(text="Г)",callback_data="Г)")

    keyboard_builder.adjust(2,2)
    return keyboard_builder.as_markup()

select_answer = get_inline_keyboard()
