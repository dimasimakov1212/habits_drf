from rest_framework import serializers

from habits.models import Habit, Prize
from habits.validators import validator_for_habit


class HabitSerializer(serializers.ModelSerializer):
    """ сериализатор для модели Habit """

    class Meta:
        model = Habit
        # exclude = ('habit_duration', )
        fields = '__all__'

        # валидаторы на правильность заполнения полей привычки
        validators = [
            validator_for_habit,
        ]


class PrizeSerializer(serializers.ModelSerializer):
    """ сериализатор для модели Prize """

    class Meta:
        model = Prize
        fields = '__all__'
