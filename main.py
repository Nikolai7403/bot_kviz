from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
import asyncio
from core.handlers.basic import get_personal_data, get_start, enter_personal_data, check_personal_data, try_again, get_job_offer
from core.handlers.quiz import quiz
from core.handlers.callback import select_answer
from core.settings import settings
from core.memoryStorage.storage import storage





async  def start():
    bot = Bot(token=settings.bots.bot_token)
    dp = Dispatcher(storage=storage)

    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(get_job_offer, F.text == 'Даю согласие', StateFilter("get_job_offer"))
    dp.message.register(get_personal_data, StateFilter("get_personal_data"))
    dp.message.register(enter_personal_data, StateFilter("enter_personal_data"))
    dp.message.register(check_personal_data, StateFilter("check_personal_data"))
    dp.callback_query.register(select_answer)
    dp.message.register(try_again, Command(commands=['tryagain']))
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


while True:
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        break
    except:
        print("я упал. ПАМАГИТЕ!!!")
