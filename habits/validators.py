from rest_framework.serializers import ValidationError
from datetime import timedelta


def validator_for_habit(value):
    """ Проверка на правильность заполнения полей привычки """

    habit_time = timedelta(minutes=2)  # задаем время выполнения привычки не более 2 минут

    try:
        if value['habit_is_nice']:
            if value['connected_habit'] or value['habit_prize']:
                raise ValidationError('У приятной привычки не может быть связанной привычки или вознаграждения')
    except KeyError:
        pass

    try:
        if value['connected_habit'] and value['habit_prize']:
            raise ValidationError('Можно выбрать или приятную привычку или вознаграждение')
    except KeyError:
        pass

    try:
        if value['habit_duration'] > habit_time:
            raise ValidationError('Привычку можно выполнять не более 2 минут')
    except KeyError:
        pass

    try:
        if value['connected_habit']:
            if not value['connected_habit'].habit_is_nice:
                raise ValidationError('В связанные привычки могут попадать только приятные привычки')
    except KeyError:
        pass
