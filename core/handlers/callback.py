from aiogram import Bot
from aiogram.types import CallbackQuery
from core.memoryStorage.storage import storage
from core.handlers.quiz import quiz_next, get_resualt
from aiogram.fsm.context import FSMContext
from core.personaldata.personaldata import record_attempt

async def select_answer(call: CallbackQuery, bot: Bot, state: FSMContext):
    correct = await storage.get_data(call.from_user.id)
    correct = correct['answer'] #Записываем правильный ответ из вопроса в переменную
    if call.data == correct:
        stor = await storage.get_data(call.from_user.id)
        attempt = stor['attempt']
        attempt += 1
        await storage.update_data(call.from_user.id, {'attempt': attempt})
        idx_attempt = stor['idx_attempt']
        record_attempt(call.from_user.id, idx_attempt, attempt)
    #Редактируем сообщение после нажатия inlineButton: убираем inline клавиатуру, изменяем текст сообщения
    msg = f"{call.message.text}\n\nВаш ответ - {call.data}" #Добавляем к сообщению ответ пользователя
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, reply_markup=None)

    if await state.get_state() == "quiz":
        await quiz_next(call, bot, state)
    elif await state.get_state() == "resualt":
        attempt = await storage.get_data(call.from_user.id)
        attempt = int(attempt['attempt'])
        await get_resualt(call.from_user.id, bot, attempt)