import aiosqlite
from aiogram import Bot, Dispatcher
import logging
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from quests import quiz_data

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
API_TOKEN = '6332505104:AAEDi9TYw0hdqvuNZpNFN8hmP9pkh3rkutQ'

# Зададим имя базы данных
DB_NAME = 'quiz_bot.db'

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()


def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )

    builder.adjust(1)
    return builder.as_markup()


# начинаем квиз
async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    questions_true = 0
    await update_quiz_index(user_id, current_question_index, questions_true)
    await get_question(message, user_id)


# Получение из БД
async def get_quiz_index(user_id):
    # Подключаемся к базе данных
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


# Обновление БД
async def update_quiz_index(user_id, index, questions_true):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index, questions_true) VALUES (?, ?, ?)',
                         (user_id, index, questions_true))
        # Сохраняем изменения
        await db.commit()


async def update_questions_true(user_id, questions_true):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('UPDATE quiz_state SET questions_true = ? WHERE user_id = ?',
                         (questions_true, user_id))
        # Сохраняем изменения
        await db.commit()


async def get_questions_true(user_id):
    # Подключаемся к базе данных
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT questions_true FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


# Функция создания БД
async def create_table():
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER, 
            questions_true INTEGER)''')
        # Сохраняем изменения
        await db.commit()


# Задаем вопрос
async def get_question(message, user_id):
    # Получение текущего вопроса из словаря состояний пользователя

    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)


# Запуск процесса поллинга новых апдейтов
async def main():
    # Запускаем создание таблицы базы данных
    await create_table()

    await dp.start_polling(bot)
