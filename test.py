from telebot import TeleBot
from telemulator3 import Telemulator, send_command
from time import sleep

from main import bot

# Emulate Telegram API for bot
telemul = Telemulator()
telemul.set_tested_bot(bot, username='my_bot', name='My Bot')

# At start, there are no registered users in emulated API.
assert not telemul.api.users

# Make API user, that represent our bot.
# It's a first registered user.
mybot = telemul.api.get_me()
assert mybot.is_bot
assert mybot.username == 'my_bot'
assert len(telemul.api.users) == 1

# New user open private chat with bot and send `/start` command.
# Bot must answer as defined and his answer must be in chat history.
user = telemul.api.create_user('User')
chat = user.private()

iteration = 0
def send_check_reply(message, reply):
    global iteration
    iteration += 2
    send_command(chat, message, user)
    sleep(0.05)
    assert reply in str(chat.history.messages[iteration])

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

# 44,1,2,130,234,0,1,179,1,0.4,2,0,2
# 1
