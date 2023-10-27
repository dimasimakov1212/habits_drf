from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from habits.models import Habit, Prize
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, PrizeSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """ создание привычки """

    serializer_class = HabitSerializer
    # queryset = Habit.objects.all()

    # доступно только авторизованным пользователям и не модераторам
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """
        Определяем порядок создания нового объекта
        """
        new_habit = serializer.save()
        new_habit.habit_owner = self.request.user  # задаем владельца привычки

        new_habit.save()


class HabitListAPIView(generics.ListAPIView):
    """ вывод списка привычек пользователя """

    serializer_class = HabitSerializer
    # pagination_class = CourseLessonPaginator  # пагинация

    # доступно только авторизованным пользователям, и владельцам
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """ Определяем параметры вывода объектов """

        queryset = Habit.objects.filter(habit_owner=self.request.user)
        return queryset

    # queryset = Habit.objects.all()

    # permission_classes = [AllowAny]


class HabitPublicListAPIView(generics.ListAPIView):
    """ вывод списка публичных привычек """

    serializer_class = HabitSerializer
    # pagination_class = CourseLessonPaginator  # пагинация

    # доступно любым пользователям
    permission_classes = [AllowAny]

    def get_queryset(self):
        """ Определяем параметры вывода объектов """

        queryset = Habit.objects.filter(habit_is_public=True)
        return queryset


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """ просмотр информации об одной привычке """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    # доступно только авторизованным пользователям, и владельцам
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """ изменение привычки """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    # доступно только авторизованным пользователям, и владельцам
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """ удаление привычки """

    queryset = Habit.objects.all()

    # доступно только авторизованным пользователям, и владельцам
    permission_classes = [IsAuthenticated, IsOwner]


class PrizeCreateAPIView(generics.CreateAPIView):
    """ создание награды """

    serializer_class = PrizeSerializer

    # доступно только авторизованным пользователям
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Определяем порядок создания нового объекта """

        new_prize = serializer.save()
        new_prize.prize_owner = self.request.user  # задаем владельца привычки

        new_prize.save()


class PrizeListAPIView(generics.ListAPIView):
    """ вывод списка наград """

    serializer_class = PrizeSerializer

    # доступно только авторизованным пользователям, и владельцам
    permission_classes = [IsAuthenticated, IsOwner]
    # permission_classes = [AllowAny]

    # pagination_class = CourseLessonPaginator  # пагинация

    def get_queryset(self):
        """ Определяем параметры вывода объектов """

        queryset = Prize.objects.filter(prize_owner=self.request.user)
        return queryset
