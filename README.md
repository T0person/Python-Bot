<p>Файл <b>main.py</b> - файл с логикой.</p>
<p><b>right_answer(callback: types.CallbackQuery)</b> - функция подсчета правильного ответа и общения с пользователем, принимает ответ на кнопку.</p>
<p><b>wrong_answer(callback: types.CallbackQuery)</b> - функция подсчета неправильного ответа и общения с пользователем, принимает ответ на кнопку.</p>
<p><b>cmd_start(message: types.Message)</b> - функция запуска бота, принимает от пользователя команду "/start".</p>
<p><b>cmd_start(message: types.Message)</b> - функция запуска квиза, принимает от пользователя команду "/quiz" или нажатие на кнопку "Начать игру".</p>
<p><b>get_result(message: types.Message)</b> - функция вывода результатов пользователя, активируется при нажатие копки "Мой результат".</p>
<p><b>get_last_result_users(message: types.Message)</b> - функция вывода результатов всех пользователей, активируется при нажатие "Посмотреть результаты всех пользователей".</p>

<p>Файл <b>func.py</b> - основной файл с функционалом.</p>
<p><b>generate_main_keyboard()</b> - функция генерации клавиатуры с двумя кнопками: "Начать игру" и "Посмотреть результаты всех пользователей".</p>
<p><b>generate_options_keyboard(answer_options, right_answer):</b> - функция генерации правильного ответа, принимает список предложенных ответов и индекс правильного ответа.</p>
<p><b>new_quiz(message)</b> - функция начала квиза, активируется при нажатии кнопки "Начать игру" или команды "/quiz".</p>
<p><b>get_quiz_index(user_id)</b> - функция подключения к БД и получения индекса следующего вопроса для пользователя.</p>
<p><b>update_quiz_index(user_id, full_name, index=0, questions_true=0, last_result=0)</b> - функция подключения к БД и обновления индекса вопроса для пользователя, принимает id пользователя, полное имя, индекс вопороса,
количество правильных ответов и последний результат теста.</p>
<p><b>get_questions_true(user_id)</b> - функция подключения к БД и получения количества правильных ответов пользователя, принимает id пользователя.</p>
<p><b>get_result_all_users()</b> - функция подключения к БД и получения последних результатов всех пользователей.</p>
<p><b>create_table()</b> - функция создания БД.</p>
<p><b>get_question(message, user_id)</b> - функция генерации вопроса и вывода на экран пользователю, принимает сообщение от пользователя и id пользователя.</p>
<p><b>main()</b> - функция запуска бота и запуска БД.</p>

<p>Файл <b>quests.py</b> - файл перечня вопросов для квиза.</p>
