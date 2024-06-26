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


bot = telebot.TeleBot(environ['KPO_TOKEN'], threaded = False)

field_descs = ["возраст", "пол (1 = М; 0 = Ж)", "тип боли в груди (4 варианта, число)", "артериальное давление в состоянии покоя", "холесторал в сыворотке, мг/дл", "уровень сахара в крови натощак > 120 мг/дл (число 0 или 1)", "результаты электрокардиографии покоя (значения 0,1,2)", "достигнута ли максимальная частота сердечных сокращений", "стенокардия, вызванная физической нагрузкой", "oldpeak = депрессия ST, вызванная физическими упражнениями, по сравнению с отдыхом", "наклон пикового сегмента ST при нагрузке", "количество магистральных сосудов (0-3), окрашенных флюороскопией", "thal: 0 = нормально; 1 = фиксированный дефект; 2 = обратимый дефект"]

filed_names = "age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal".split(',')

def handle_value_error(message):
    bot.reply_to(message, 'Слушайте введите число а. Дробную часть писать через точку')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать! Пожалуйста, введите значения полей в последовательных сообщениях (age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal). В результате мы вам ответим предположением о наличии заболеваний. Начните вводить ' + field_descs[0] + '.')

@bot.message_handler(commands=['update'])
def update_filed(message):
    user_id = message.chat.id
    if 'user_data' not in globals() or user_id not in user_data:
        bot.reply_to(message, 'Вас еще нет')
        return
    
    parts = message.text.split()
    if len(parts) < 3:
        bot.reply_to(message, 'usage: /update age 18')
        return
    field = parts[1]
    value = parts[2]

    step = len(user_data[user_id])
    i = 0
    while i < len(filed_names):
        if filed_names[i] == field:
            break
        i += 1
    if i == len(filed_names):
        bot.reply_to(message, 'Нет такого поля')
        return
    if i > step:
        bot.reply_to(message, 'У вас еще нет этого поля')
        return
    
    try:
        value = float(value)
    except ValueError:
        handle_value_error(message)
        return
    user_data[user_id][i] = value

def predict(user_id):
    if 'user_data' not in globals() or user_id not in user_data:
        bot.send_message(user_id, 'Вас еще нет')
        return
    if len(user_data[user_id]) == len(field_descs):
        prediction = model.predict(np.array(user_data[user_id]).reshape(1, -1))[0]
        bot.send_message(user_id, 'Вы' + (' не' if prediction == 0 else '') + ' больны')
    else:
        bot.send_message(user_id, 'У вас еще не все поля')

@bot.message_handler(commands=['predict'])
def handle_predict_command(message):
    predict(message.chat.id)

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
    
    if step > len(field_descs) - 1:
        bot.reply_to(message, 'Все вы все заполнили что вам еще надо?? Ну можно обновлять поля (/update age 18). Еще раз узнать результат будет /predict')
        return

    try:
        value = float(raw)
    except ValueError:
        handle_value_error(message)
        return
    
    if value != None:
        user_data[user_id].append(value)

    if step == len(field_descs) - 1:
        predict(user_id)
    else:
        bot.send_message(user_id, 'Введите ' + field_descs[(step + 1) % len(field_descs)])

if __name__ == "__main__":
    bot.polling()
