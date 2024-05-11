from telebot import TeleBot
from telemulator3 import Telemulator, send_command

from main import bot

telemul = Telemulator()
telemul.set_tested_bot(bot, username='my_bot', name='My Bot')

assert not telemul.api.users

mybot = telemul.api.get_me()
assert mybot.is_bot
assert mybot.username == 'my_bot'

assert len(telemul.api.users) == 1

def test_main_user_scenario_predict(call_n):
    user = telemul.api.create_user('User' + str(call_n))
    chat = user.private()
    iteration = 0
    def send_check_reply(message, reply):
        nonlocal iteration
        iteration += 2
        send_command(chat, message, user)
        assert reply in str(chat.history.messages[iteration])
    # 44,1,2,130,234,0,1,179,1,0.4,2,0,2
    send_check_reply('/start', "Начните вводить возраст")
    send_check_reply('44', "Введите пол")
    send_check_reply('1', "Введите тип боли")
    send_check_reply('2', "артериальное давление")
    send_check_reply('130', "холесторал в сыворотке")
    send_check_reply('234', "уровень сахара")
    send_check_reply('0', "результаты электрокардиографии")
    send_check_reply('1', "максимальная частота сердечных")
    send_check_reply('179', "стенокардия")
    send_check_reply('1', "oldpeak")
    send_check_reply('0.4', "наклон пикового сегмента")
    send_check_reply('2', "магистральных сосудов")
    send_check_reply('0', "thal")
    send_check_reply('2', "Вы больны")
    send_check_reply('/predict', "Вы больны")

def test_update_all_scenarios(call_n):
    user = telemul.api.create_user('User' + str(call_n))
    chat = user.private()
    send_command(chat, '42', user)
    send_command(chat, "/update age 52", user)
    assert len(chat.history.messages) == 3
    send_command(chat, "/update thal 52", user)
    assert 'У вас еще нет этого поля' in str(chat.history.messages[5])
    send_command(chat, "/update asd 52", user)
    assert 'Нет такого поля' in str(chat.history.messages[7])

test_functions = [test_main_user_scenario_predict, test_update_all_scenarios]
for i in range(len(test_functions)):
    test_functions[i](i)
