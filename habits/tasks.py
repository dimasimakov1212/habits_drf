from datetime import datetime

import pytz
from celery import shared_task

from habits.models import Habit
from habits.services import create_massage


@shared_task
def check_habits_daily():
    """ проверка ежедневных привычек на выполнение """

    date_time_now = datetime.now()  # получаем текущие дату и время
    moscow_timezone = pytz.timezone('Europe/Moscow')  # устанавливаем часовой пояс
    date_now = date_time_now.astimezone(moscow_timezone)  # устанавливаем текущую дату с учетом часового пояса
    time_now = date_now.time()  # получаем текущее время
    # print(time_now)

    # получаем разницу во времени между временем привычки и текущим временем в минутах
    # time_delta = round(
    #     (datetime.combine(date_now, habit_time) - datetime.combine(date_now, time_now)).total_seconds()
    # ) / 60

    # получаем полезные привычки по заданному времени дня и периодичности выполнения
    habits = Habit.objects.filter(habit_time__hour=time_now.hour, habit_time__minute=time_now.minute,
                                  habit_period='ежедневно', habit_is_nice=False)

    for habit in habits:
        create_massage(habit.id)  # создаем сообщение для дальнейшей отправки в бот


@shared_task
def check_habits_weekly():
    """ проверка еженедельных привычек на выполнение """

    date_time_now = datetime.now()  # получаем текущие дату и время
    moscow_timezone = pytz.timezone('Europe/Moscow')  # устанавливаем часовой пояс
    date_now = date_time_now.astimezone(moscow_timezone)  # устанавливаем текущую дату с учетом часового пояса
    time_now = date_now.time()  # получаем текущее время
    # print(time_now)

    habits = Habit.objects.filter(habit_time__hour=time_now.hour, habit_time__minute=time_now.minute,
                                  habit_period='еженедельно', habit_is_nice=False)

    for habit in habits:
        create_massage(habit.id)  # создаем сообщение для дальнейшей отправки в бот
