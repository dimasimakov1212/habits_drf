from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора для модели Habit
    """

    class Meta:
        model = Habit
        # exclude = ('habit_duration', )
        fields = '__all__'

    # def get_lessons(self, course):
    #     """
    #     Метод определения поля lessons
    #     :return: список уроков курса
    #     """
    #     lessons = [lesson.lesson_title for lesson in Lesson.objects.filter(course=course)]
    #     return lessons

