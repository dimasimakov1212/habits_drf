from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit, Prize
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        # создаем тестового пользователя
        self.user = User.objects.create(user_email='admin@sky.pro')
        self.user.set_password('dima123')
        self.user.save()

        # аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """ тестирование создания привычки """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"user_email": "admin@sky.pro", "password": "dima123"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # задаем данные для создания привычки
        data_habit = {
            'habit_user': 'Test',
            'habit_name': 'Test',
            'habit_action': 'Test',
            'habit_is_nice': True,
            'habit_period': 'ежедневно',
            'habit_owner': self.user.pk
        }

        # создаем привычку
        response = self.client.post(
            '/habits/habit_create/',
            data=data_habit
        )

        # print(response.json())

        # проверяем ответ на создание привычки
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # проверяем ответ на соответствие сохраненных данных
        self.assertEquals(
            response.json(),
            {'id': 2, 'habit_user': 'Test', 'habit_name': 'Test', 'habit_place': None, 'habit_time': None,
             'habit_action': 'Test', 'habit_is_nice': True, 'habit_period': 'ежедневно', 'habit_duration': '00:02:00',
             'habit_is_public': False, 'connected_habit': None, 'habit_prize': None, 'habit_owner': 2}
        )

        # проверяем на существование объектов привычек
        self.assertTrue(
            Habit.objects.all().exists()
        )

    def test_list_habit(self):
        """ тестирование списка привычек """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"user_email": "admin@sky.pro", "password": "dima123"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # создаем тестовую привычку
        Habit.objects.create(
            habit_user='Test',
            habit_name='Test',
            habit_action='Test',
            habit_is_nice=True,
            habit_period='ежедневно',
            habit_owner=self.user
        )

        # получаем список привычек
        response = self.client.get(
            '/habits/'
        )

        # print(response.json())

        # проверяем ответ на получение списка привычек
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # проверяем ответ на соответствие сохраненных данных
        self.assertEquals(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [{'id': 5, 'habit_user': 'Test',
                                                                      'habit_name': 'Test', 'habit_place': None,
                                                                      'habit_time': None, 'habit_action': 'Test',
                                                                      'habit_is_nice': True,
                                                                      'habit_period': 'ежедневно',
                                                                      'habit_duration': '00:02:00',
                                                                      'habit_is_public': True, 'connected_habit': None,
                                                                      'habit_prize': None, 'habit_owner': 5}]}

        )

    def test_detail_habit(self):
        """ тестирование информации о привычке """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"user_email": "admin@sky.pro", "password": "dima123"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # создаем тестовую привычку
        habit = Habit.objects.create(
            habit_user='Test',
            habit_name='Test',
            habit_action='Test',
            habit_is_nice=True,
            habit_period='ежедневно',
            habit_owner=self.user
        )

        # получаем детали привычки
        response = self.client.get(
            reverse('habits:habit_detail', kwargs={'pk': habit.pk})
        )

        # print(response.json())

        # проверяем ответ на получение привычки
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # проверяем ответ на соответствие сохраненных данных
        self.assertEquals(
            response.json(),
            {'id': 4, 'habit_user': 'Test', 'habit_name': 'Test', 'habit_place': None, 'habit_time': None,
             'habit_action': 'Test', 'habit_is_nice': True, 'habit_period': 'ежедневно', 'habit_duration': '00:02:00',
             'habit_is_public': True, 'connected_habit': None, 'habit_prize': None, 'habit_owner': 4}
        )

    def test_change_habit(self):
        """ тестирование изменения привычки """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"user_email": "admin@sky.pro", "password": "dima123"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # создаем тестовую привычку
        habit = Habit.objects.create(
            habit_user='Test',
            habit_name='Test',
            habit_action='Test',
            habit_is_nice=True,
            habit_period='ежедневно',
            habit_owner=self.user
        )

        # данные для изменения привычки
        data_habit_change = {
            'habit_user': 'Test_1',
        }

        # получаем детали привычки
        response = self.client.patch(
            reverse('habits:habit_change', kwargs={'pk': habit.pk}),
            data=data_habit_change
        )

        # print(response.json())

        # проверяем ответ на получение привычки
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # проверяем ответ на соответствие сохраненных данных
        self.assertEquals(
            response.json(),
            {'id': 1, 'habit_user': 'Test_1', 'habit_name': 'Test', 'habit_place': None, 'habit_time': None,
             'habit_action': 'Test', 'habit_is_nice': True, 'habit_period': 'ежедневно', 'habit_duration': '00:02:00',
             'habit_is_public': True, 'connected_habit': None, 'habit_prize': None, 'habit_owner': 1}
        )

    def test_delete_habit(self):
        """ тестирование удаления привычки """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"user_email": "admin@sky.pro", "password": "dima123"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # создаем тестовую привычку
        habit = Habit.objects.create(
            habit_user='Test',
            habit_name='Test',
            habit_action='Test',
            habit_is_nice=True,
            habit_period='ежедневно',
            habit_owner=self.user
        )

        # получаем детали привычки
        response = self.client.delete(
            reverse('habits:habit_delete', kwargs={'pk': habit.pk})
        )

        # проверяем ответ на получение привычки
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class PrizeTestCase(APITestCase):

    def setUp(self) -> None:
        # создаем тестового пользователя
        self.user = User.objects.create(user_email='admin@sky.pro')
        self.user.set_password('dima123')
        self.user.save()

        # аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

    def test_create_prize(self):
        """ тестирование создания награды """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"user_email": "admin@sky.pro", "password": "dima123"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # задаем данные для создания награды
        data_prize = {
            'prize_name': 'Test',
            'prize_description': 'Test',
            'prize_owner': self.user.pk
        }

        # создаем награду
        response = self.client.post(
            '/habits/prize_create/',
            data=data_prize
        )

        # print(response.json())

        # проверяем ответ на создание награды
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # проверяем ответ на соответствие сохраненных данных
        self.assertEquals(
            response.json(),
            {'id': 2, 'prize_name': 'Test', 'prize_description': 'Test', 'prize_owner': 7}
        )

        # проверяем на существование объектов
        self.assertTrue(
            Prize.objects.all().exists()
        )

    def test_list_prize(self):
        """ тестирование списка наград """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"user_email": "admin@sky.pro", "password": "dima123"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # создаем тестовую награду
        Prize.objects.create(
            prize_name='Test',
            prize_description='Test',
            prize_owner=self.user
        )

        # получаем список наград
        response = self.client.get(
            '/habits/prizes/'
        )

        # print(response.json())

        # проверяем ответ на получение списка объектов
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # проверяем ответ на соответствие сохраненных данных
        self.assertEquals(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [{'id': 5, 'prize_name': 'Test',
                                                                      'prize_description': 'Test', 'prize_owner': 10}]}
        )

    def test_detail_prize(self):
        """ тестирование информации о награде """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"user_email": "admin@sky.pro", "password": "dima123"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # создаем тестовую награду
        prize = Prize.objects.create(
            prize_name='Test',
            prize_description='Test',
            prize_owner=self.user
        )

        # получаем детали награды
        response = self.client.get(
            reverse('habits:prize_detail', kwargs={'pk': prize.pk})
        )

        # print(response.json())

        # проверяем ответ на получение объекта
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # проверяем ответ на соответствие сохраненных данных
        self.assertEquals(
            response.json(),
            {'id': 4, 'prize_name': 'Test', 'prize_description': 'Test', 'prize_owner': 9}
        )

    def test_change_prize(self):
        """ тестирование изменения награды """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"user_email": "admin@sky.pro", "password": "dima123"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # создаем тестовую награду
        prize = Prize.objects.create(
            prize_name='Test',
            prize_description='Test',
            prize_owner=self.user
        )

        # данные для изменения привычки
        data_prize_change = {
            'prize_name': 'Test_1',
        }

        # получаем детали привычки
        response = self.client.patch(
            reverse('habits:prize_change', kwargs={'pk': prize.pk}),
            data=data_prize_change
        )

        # print(response.json())

        # проверяем ответ на получение привычки
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # проверяем ответ на соответствие сохраненных данных
        self.assertEquals(
            response.json(),
            {'id': 1, 'prize_name': 'Test_1', 'prize_description': 'Test', 'prize_owner': 6}
        )

    def test_delete_prize(self):
        """ тестирование удаления награды """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"user_email": "admin@sky.pro", "password": "dima123"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # создаем тестовую награду
        prize = Prize.objects.create(
            prize_name='Test',
            prize_description='Test',
            prize_owner=self.user
        )

        # получаем детали награды
        response = self.client.delete(
            reverse('habits:prize_delete', kwargs={'pk': prize.pk})
        )

        # проверяем ответ на получение привычки
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
