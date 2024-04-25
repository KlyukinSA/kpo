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
    bot.send_message(message.chat.id, 'Добро пожаловать! Пожалуйста, введите значения полей в последовательных сообщениях  (age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal). В результате мы вам ответим предположением о наличии заболеваний. Начните вводить age.')

@bot.message_handler(content_types='text')
def input_one(message):
    global user_data
    if 'user_data' not in globals():
        user_data = {}

    user_id = message.chat.id
    print("user_id",user_id)

    if user_id not in user_data:
        user_data[user_id] = []

    print(user_data[user_id])
    user_data[user_id].append(message.text)
    print(len(user_data[user_id]))

    if len(user_data[user_id]) == 13:  # Должно быть 13 полей
        user_input = [float(value) for value in user_data[user_id]]
        prediction = model.predict([user_input])[0]
        bot.reply_to(message, f"Предсказанное значение целевой переменной (target): {prediction}")
        del user_data[user_id]
    
bot.polling()
