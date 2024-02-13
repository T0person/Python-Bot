import asyncio

from aiogram import types

from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from func import (main, get_quiz_index, update_quiz_index, get_question, new_quiz, quiz_data, dp, get_questions_true,
                  get_result_all_users, generate_main_keyboard)


# Хендлер Правильный ответ
@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    await callback.message.answer("Верно!")
    # Получаю индекс
    current_question_index = await get_quiz_index(callback.from_user.id)
    # Обновляю количество правильных ответов
    questions_true = await get_questions_true(callback.from_user.id)
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    # Обновление правильных вопросов
    questions_true += 1
    # Добавление индекса
    await update_quiz_index(callback.from_user.id, callback.from_user.full_name, current_question_index, questions_true)
    # Добавление правильного ответа
    await update_quiz_index(callback.from_user.id, callback.from_user.full_name, current_question_index, questions_true)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        # Заполенение конечного результата
        await update_quiz_index(callback.from_user.id, callback.from_user.full_name, current_question_index, questions_true, questions_true)
        # Создание базовых кнопок
        keyboard = generate_main_keyboard()
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nПравильных ответов: {questions_true}",
                                      reply_markup=keyboard)


# Хендлер Неправильный ответ
@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    # Получение правильных вопросов
    questions_true = await get_questions_true(callback.from_user.id)
    # Получение правильного ответа
    correct_option = quiz_data[current_question_index]['correct_option']
    # Ответочка
    await callback.message.answer(
        f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    # Следующий вопрос
    await update_quiz_index(callback.from_user.id, callback.from_user.full_name, current_question_index, questions_true)
    # Некст или конец
    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        # Заполнение конечного результата
        await update_quiz_index(callback.from_user.id, callback.from_user.full_name, current_question_index, questions_true, questions_true)
        # Создание базовых кнопок
        keyboard = generate_main_keyboard()
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nПравильных ответов: {questions_true}",
                                      reply_markup=keyboard)


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Делаю жирным имя пользователя
    content = Text(
        'Привет, ',
        Bold(message.from_user.full_name),
        '\nДобро пожаловать в квиз!'
    )
    # Создаю базовые кнопки
    keyboard = generate_main_keyboard()
    await message.answer(**content.as_kwargs(), reply_markup=keyboard)


# Хэндлер на команду /quiz
@dp.message(F.text == "Начать игру")
@dp.message(Command("quiz"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Мой результат"))

    await message.answer(f"Давайте начнем квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

    await new_quiz(message)


@dp.message(F.text == 'Мой результат')
async def get_result(message: types.Message):
    text = await get_questions_true(message.from_user.id)
    await message.answer('Не было правильного ответа на вопросы') if text == 0 else await message.answer(f"Правильных ответов: {text}")

@dp.message(F.text == 'Посмотреть результаты всех пользователей')
async def get_last_result_users(message: types.Message):
    last_result_users = await get_result_all_users()
    text = ''
    for user, result in last_result_users:
        text += f'Пользователь: {user} правильно ответил на {result} вопросов\n'
        
    await message.answer(text)



if __name__ == "__main__":
    asyncio.run(main())
