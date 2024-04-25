import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

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


from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from os import environ

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Добро пожаловать! Пожалуйста, введите значения полей через запятую (age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal):')

def predict(update: Update, context: CallbackContext) -> None:
    input_data = update.message.text
    input_list = list(map(float, input_data.split(',')))

    prediction = model.predict([input_list])[0]
    update.message.reply_text(f"Предполагаемый результат target: {prediction}")

def main() -> None:
    updater = Updater(environ['KPO_TOKEN'])

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, predict))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
