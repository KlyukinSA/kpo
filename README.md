# kpo

Телеграм бот использует ML и содержит следующий функционал.

Система выявления сердечных заболеваний

Пользователь делает запрос для получения результата. Запрос содержит поля, относящиеся к человеку, заболевание которого надо выявить:
1. возраст
2. пол
3. тип боли в груди (4 варианта)
4. артериальное давление в состоянии покоя
5. холесторал в сыворотке, мг/дл
6. уровень сахара в крови натощак > 120 мг/дл
7. результаты электрокардиографии покоя (значения 0,1,2)
8. достигнута максимальная частота сердечных сокращений
9. стенокардия, вызванная физической нагрузкой
10. oldpeak = депрессия ST, вызванная физическими упражнениями, по сравнению с отдыхом
11. наклон пикового сегмента ST при нагрузке
12. количество магистральных сосудов (0-3), окрашенных флюороскопией
13. thal: 0 = нормально; 1 = фиксированный дефект; 2 = обратимый дефект

Система отвечает предположением о наличии заболеваний.

# Участники проекта

- Клюкин Степан
- Шеремет Сергей
группа 5130904/10102

# Тестирование

1. старт

ввести "/start"

ответит "Добро пожаловать! Пожалуйста, введите значения полей в последовательных сообщениях (age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal). В результате мы вам ответим предположением о наличии заболеваний. Начните вводить возраст."

2. ввести какоенибудь число

ввести "42"

ответит "Введите пол (1 = М; 0 = Ж)"

3. попробовать обновить свой возраст

"/update age 52"

ничего не ответит

4. попробовать обновить свой thal

"/update thal 52"

"У вас еще нет этого поля"

5. попробовать обновить поле которого нет

"Нет такого поля"

6. заполнить уже свои поля до конца

Можно отправить боту следующие две последовательности:
```
52,1,0,128,203,1,1,156,1,1,1,0,0
44,1,2,130,234,0,1,179,1,0.4,2,0,2
```
Они взяты из обучающей выборки но с небольшими изменениями. Первая должна выдать результат что не болен, а вторая что болен.

7. предсказать свой рез вот просто так еще раз

"/predict"

"Вы больны"

# Запуск

1. скачать датасет и поместить его в директорию, из которой будете запускать python: https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset?resource=download&select=heart.csv
2. установить все библиотеки конечно. e g `pip install pyTelegramBotAPI`
3. установить переменную среды в токен вашего бота: `export KPO_TOKEN=54564:AASD-Y-afs546af4s6d5`
4. запустить питон
