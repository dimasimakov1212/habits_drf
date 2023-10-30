import requests
from django.http import HttpResponse
import time

from config.settings import TELEGRAM_ACCESS_TOKEN, TELEGRAM_CHAT_ID
from habits.models import Habit

bot_token = TELEGRAM_ACCESS_TOKEN
tg_chat_id = TELEGRAM_CHAT_ID
get_id_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'  # url для получения данных чата
send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'  # url для отправки сообщений


def send_message_to_bot(chat_id, message):
    """ функция отправки сообщения в телеграм-бот
    chat_id: id чата
    message: передаваемое сообщение
    """

    params = {"chat_id": chat_id, "text": message}

    response = requests.get(send_message_url, params=params).json()

    return response


def create_massage(habit_id):
    """ функция создания сообщения для отправки в телеграм-бот """

    habit = Habit.objects.get(id=habit_id)  # получаем привычку

    user = habit.habit_user  # имя получателя сообщения
    habit_time = habit.habit_time  # время выполнения привычки
    action = habit.habit_action  # действие привычки, которое необходимо выполнить
    place = habit.habit_place  # место выполнения привычки
    duration = round(habit.habit_duration.total_seconds() / 60)  # длительность выполнения привычки в минутах

    message = f'Привет {user} ! Скоро надо сделать {action} в {habit_time} {place}. Надо успеть за {duration} минут'

    response = send_message_to_bot(tg_chat_id, message)  # отправляем сообщение

    # проверяем есть ли у полезной привычки связанная приятная привычка или награда
    if habit.connected_habit or habit.habit_prize:

        # получаем данные о связанной привычке и отправляем сообщение пользователю
        if habit.connected_habit:
            nice_habit_id = habit.connected_habit.id
            nice_habit = Habit.objects.get(id=nice_habit_id)

            # длительность выполнения привычки в минутах
            nice_time = round(nice_habit.habit_duration.total_seconds() / 60)

            nice_message = (f'Если ты вополнил полезную привычку, ты можешь {nice_habit.habit_action} '
                            f'в течение {nice_time} минут')

            time.sleep(10)
            nice_response = send_message_to_bot(tg_chat_id, nice_message)  # отправляем сообщение

            return HttpResponse(nice_response)

        # получаем данные о награде и отправляем сообщение пользователю
        if habit.habit_prize:
            prize_message = f'Если ты вополнил полезную привычку, ты можешь {habit.habit_prize.prize_description}'

            time.sleep(10)
            nice_response = send_message_to_bot(tg_chat_id, prize_message)  # отправляем сообщение

            return HttpResponse(nice_response)

    # print(response)

    return HttpResponse(response)


def get_bot_id():
    """ получения данных чата """

    response = requests.get(get_id_url).json()

    # print(response)

    return HttpResponse(response)
