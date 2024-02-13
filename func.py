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


def generate_main_keyboard():
    kb = [[
        types.KeyboardButton(text="Начать игру"),
        types.KeyboardButton(text="Посмотреть результаты всех пользователей")
    ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


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
    await update_quiz_index(message.from_user.id, message.from_user.full_name)
    await get_question(message, message.from_user.id)


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
async def update_quiz_index(user_id, full_name, index=0, questions_true=0, last_result=0):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, full_name, question_index, questions_true, last_result) VALUES (?, ?, ?, ?, ?)',
            (user_id, full_name, index, questions_true, last_result))
        # Сохраняем изменения
        await db.commit()


async def get_questions_true(user_id):
    # Подключаемся к базе данных
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        try:
            async with db.execute('SELECT questions_true FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
                # Возвращаем результат
                results = await cursor.fetchone()
                if results is not None:
                    return results[0]
                else:
                    return 0
        except:
            return 0


async def get_result_all_users():
    # Подключаемся к базе данных
    async with aiosqlite.connect(DB_NAME) as db:
        # Получение имени пользователя и ответы
        async with db.execute("SELECT full_name, last_result FROM quiz_state") as cursor:
            return await cursor.fetchall()


# Функция создания БД
async def create_table():
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, full_name NCHAR, question_index INTEGER, 
            questions_true INTEGER, last_result INTEGER)''')
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
