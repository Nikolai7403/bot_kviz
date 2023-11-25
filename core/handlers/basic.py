import aiofiles
from aiogram import Bot
from aiogram.types import Message, InputFile
from Discription import discription
from core.utils.commands import set_commands
from aiogram.fsm.context import FSMContext
from core.keyboards.reply import reply_markup, reply_correct, reply_job
from core.memoryStorage.storage import storage
from core.personaldata.personaldata import add_csv, check_user_register, try_counter, give_attemp_index, counter_attempt
from core.handlers.quiz import get_random_numbers, quiz
from aiogram.types.input_file import BufferedInputFile


async def get_start(message: Message, bot: Bot, state: FSMContext):
    await set_commands(bot)
    await message.answer(f"{discription['Hello']}")
    if not check_user_register(message.from_user.id):
        await bot.send_message(message.chat.id, text=discription['privacy_policy'], parse_mode="HTML", reply_markup=reply_markup)
        #await state.set_state("get_personal_data")
        await state.set_state("get_job_offer")
    else:
        if counter_attempt(message.from_user.id) == 0:
            await bot.send_message(message.from_user.id, text="Попытки закончились")
            return
        await bot.send_message(chat_id=message.chat.id, text="Вы уже зарегистрированы! Переходим к квизу:", reply_markup=None)
        await storage.update_data(message.from_user.id, {"data": get_random_numbers(71)})
        await state.set_state("quiz")
        try_counter(message.from_user.id)
        await storage.update_data(message.from_user.id, {'idx_attempt': give_attemp_index(message.from_user.id)})
        await storage.update_data(message.from_user.id, {'attempt': 0})
        await quiz(message, bot, state)

async def get_job_offer(message: Message, bot: Bot, state: FSMContext):
    await message.answer(discription['get_job_offer'], reply_markup=reply_job)
    await state.set_state("get_personal_data")

async def get_personal_data(message: Message, state: FSMContext):
    await message.answer(f"{discription['get_personal_data']}")
    await state.set_state("enter_personal_data")
    msg = message.text
    await storage.update_data(message.from_user.id, {'job':msg})

async def enter_personal_data(message: Message, bot: Bot, state: FSMContext):
    title = ["Фамилия Имя", "Компания", "Должность", "Email"]
    msg_text = ""
    msg = message.text
    row = msg.split("\n")

    if len(row) < 4: #Если после сплита меньше 4-х элементов, возможно пользователь ввел данные через пробел
        row = msg.split(" ") #Производим сплит через пробел
        row[0] = row[0] + " " + row.pop(1) #Соединяем Фамилию и Имя в один элемент

    #if len(row) == 3: #Если элемента 3, то пользователь не ввел email, вместо email ставим "-"
    #    row.append("-")
    if len(row) != 4: #Если в списке НЕ 4 элемента, значит пользователь не ввел обязательные данные
        row = str(row)[1:-1]
        await bot.send_message(chat_id=message.chat.id, text=f"Вы ввели данные неверно: {row}, \nНеобходимо ввести: \n'Фамилия Имя', \n'Компания', \n'Должность', \n'Email'")
        return

    for i in range(len(title)):
        msg_text += title[i] + ": " + row[i] + "\n"

    await bot.send_message(chat_id=message.chat.id, text=f"Проверьте введеные данные: \n{msg_text}",reply_markup=reply_correct)
    row.insert(0, message.from_user.id)
    row.append(3) #Добавляем количество попыток равное 3
    row.append("-") #Заполняем попытки прочерками
    row.append("-") #Заполняем попытки прочерками
    row.append("-") #Заполняем попытки прочерками
    job_offer = await storage.get_data(message.from_user.id)
    job_offer = job_offer['job']
    row.append(job_offer)
    await storage.update_data(message.from_user.id, {'data':row})
    await state.set_state("check_personal_data")

async def check_personal_data(message: Message, state: FSMContext, bot: Bot):
    if message.text == "Всё верно":
        data = await storage.get_data(message.chat.id)
        add_csv("PersonalData.csv", data['data'])
        await message.answer("Переходим к квизу:", reply_markup=None)
        await storage.update_data(message.from_user.id, {"data": get_random_numbers(71)})
        try_counter(message.from_user.id)
        await storage.update_data(message.from_user.id, {'idx_attempt': give_attemp_index(message.from_user.id)})
        await storage.update_data(message.from_user.id, {'attempt': 0})
        await state.set_state("quiz")
        await quiz(message, bot, state)

    elif message.text == "Ввести ещё раз":
        await state.set_state("enter_personal_data")
        await message.reply("Введите данные заново")

    else:
        await message.reply("Нажмите на один из предложенных вариантов", reply_markup=reply_correct)
        return


async def try_again(message: Message, bot: Bot,state: FSMContext):
    if not check_user_register(message.from_user.id):
        await bot.send_message(chat_id=message.chat.id, text="Вы еще не зарегистрированы. Пройдите регистрацию - /start")
    else:
        count = counter_attempt(message.from_user.id)
        if count != 0:
            await bot.send_message(chat_id=message.chat.id, text=f"Оставшиеся количество попыток: {count}")
            #Запуск квиза
            await storage.update_data(message.from_user.id, {"data": get_random_numbers(71)})
            await state.set_state("quiz")
            try_counter(message.from_user.id)
            await storage.update_data(message.from_user.id, {'idx_attempt': give_attemp_index(message.from_user.id)})
            await storage.update_data(message.from_user.id, {'attempt': 0})
            await quiz(message, bot, state)

        elif count == 0:
            await bot.send_message(message.from_user.id, text="Попытки закончились")
            return
