import requests
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.settings import TELEGRAM_ACCESS_TOKEN, TELEGRAM_CHAT_ID
from habits.models import Habit

bot_token = TELEGRAM_ACCESS_TOKEN
chat_id = TELEGRAM_CHAT_ID
get_id_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'


def send_message_to_bot(self):
    """ функция отправки сообщения в телеграм-бот """

    habit = Habit.objects.get(id=6)

    user = habit.habit_user
    time = habit.habit_time
    action = habit.habit_action
    place = habit.habit_place

    message = f'Привет {user} ! Скоро надо сделать {action} в {time} {place}'

    send_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    params = {"chat_id": chat_id, "text": message}

    response = requests.get(send_url, params=params).json()

    # print(response)

    return HttpResponse(response)


def get_bot_id(self):

    response = requests.get(get_id_url).json()

    # print(response)

    return HttpResponse(response)
