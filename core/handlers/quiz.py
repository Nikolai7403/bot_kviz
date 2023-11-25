from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from Discription import discription
from core.utils.commands import set_commands
from aiogram.fsm.context import FSMContext
from core.keyboards.reply import reply_markup, reply_correct
from core.memoryStorage.storage import storage
from core.personaldata.personaldata import add_csv
from core.keyboards.inline import select_answer
import json
import random

def get_random_numbers(n): #Рандомим номера вопросов
    numbers = list(range(1, n+1))
    random.shuffle(numbers)
    return numbers[:10] #Возращаем масив наполненный 10-ю значениями

async def quiz(message: Message, bot: Bot, state: FSMContext):
    with open('question.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    index = await storage.get_data(message.from_user.id)
    index = index['data']
    i = index.pop(0)
    await bot.send_message(message.chat.id, text=f"{data[str(i)]['question']}\n{data[str(i)]['answers']}", reply_markup=select_answer)
    await storage.update_data(message.from_user.id,{'data':index})
    await storage.update_data(message.from_user.id, {'answer':data[str(i)]['correct']})


async def quiz_next(call: CallbackQuery, bot: Bot, state: FSMContext):
    with open('question.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    index = await storage.get_data(call.from_user.id)
    index = index['data']
    i = index.pop(0)
    await bot.send_message(call.message.chat.id, text=f"{data[str(i)]['question']}\n{data[str(i)]['answers']}", reply_markup=select_answer)
    await storage.update_data(call.from_user.id,{'data':index})
    await storage.update_data(call.from_user.id, {'answer':data[str(i)]['correct']})
    if len(index) == 0:
        await state.set_state("resualt")

async def get_resualt(user_id, bot: Bot, point):
    if point >= 8:

        text = f"Класс! {point} баллов — отличный результат. А за прохождение квиза дарим маленького гуся. Забрать подарок можешь на стенде Звука."
        await bot.send_message(user_id, text=f"{text}\n{discription['more']}")
    elif point >= 5 and point <= 7:
        text = f"Класс! {point} баллов — хороший результат. А за прохождение квиза дарим сумку с гусями. Забрать подарок можешь на стенде Звука."
        await bot.send_message(user_id, text=f"{text}\n{discription['more']}")
    elif point >= 2 and point <= 4:
        text = f"Ого! {point} балла — хороший результат. А за прохождение квиза дарим носки! Забрать подарок можешь на стенде Звука."
        await bot.send_message(user_id, text=f"{text}\n{discription['more']}")
    elif point == 0:
        text = f"Бывает! У тебя — {point} баллов. Давай попробуем ещё раз, чтобы точно выиграть подарок."
        await bot.send_message(user_id, text=f"{text}\n{discription['more']}")
    elif point == 1:
        text = f"Бывает! У тебя — {point} балл. Давай попробуем ещё раз, чтобы точно выиграть подарок."
        await bot.send_message(user_id, text=f"{text}\n{discription['more']}")

    await bot.send_message(user_id, text=discription['thanks'], reply_markup=None)

async def get_best_resualt(user_id, bot: Bot):
    pass