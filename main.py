import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from os import environ
import telebot

data = pd.read_csv("heart.csv")

X = data.drop('target', axis=1).to_numpy()
y = data['target']

model = RandomForestClassifier()
model.fit(X, y)

def cli():
    input_data = input("Введите значения полей через запятую (age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal): ")
    input_list = list(map(float, input_data.split(',')))

    prediction = model.predict([input_list])[0]

    print(f"Предполагаемый результат target: {prediction}")


bot = telebot.TeleBot(environ['KPO_TOKEN'])

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать! Пожалуйста, введите значения полей в последовательных сообщениях (age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal). В результате мы вам ответим предположением о наличии заболеваний. Начните вводить age.')

@bot.message_handler(content_types='text')
def input_one(message):
    global user_data
    if 'user_data' not in globals():
        user_data = {}

    user_id = message.chat.id

    if user_id not in user_data:
        user_data[user_id] = [] # 44,1,2,130,234,0,1,179,1,0.4,2

    raw = message.text
    value = None

    step = len(user_data[user_id])
    
    # if step == 9:
    try:
        value = float(raw)
    except ValueError:
        bot.reply_to(message, 'Слушайте введите число а. Дробную часть писать через точку.')
        return
    
    if value != None:
        user_data[user_id].append(value)

    if step == 12:  # Должно быть 13 полей
        prediction = model.predict(np.array(user_data[user_id]).reshape(1, -1))[0]
        bot.send_message(user_id, 'Вы' + (' не' if prediction == 0 else '') + ' больны')
        del user_data[user_id]
    
bot.polling()
