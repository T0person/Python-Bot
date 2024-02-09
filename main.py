import asyncio

from aiogram import types

from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from func import (main, get_quiz_index, update_quiz_index, get_question, new_quiz, quiz_data, dp, get_questions_true,
                  update_questions_true)


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
    questions_true += 1

    await update_quiz_index(callback.from_user.id, current_question_index, questions_true)
    await update_questions_true(callback.from_user.id, questions_true)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        questions_true = await get_questions_true(callback.from_user.id)
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nПравильных ответов: {questions_true}")


@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    questions_true = await get_questions_true(callback.from_user.id)

    correct_option = quiz_data[current_question_index]['correct_option']

    await callback.message.answer(
        f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1

    await update_quiz_index(callback.from_user.id, current_question_index, questions_true)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nПравильных ответов: {questions_true}")


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))

    # Делаю жирным имя пользователя
    content = Text(
        'Привет, ',
        Bold(message.from_user.full_name),
        '\nДобро пожаловать в квиз!'
    )
    await message.answer(**content.as_kwargs(), reply_markup=builder.as_markup(resize_keyboard=True))


# Хэндлер на команду /quiz
@dp.message(F.text == "Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!", reply_markup=types.ReplyKeyboardRemove())

    await new_quiz(message)


if __name__ == "__main__":
    asyncio.run(main())
