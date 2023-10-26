from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitCreateAPIView, HabitListAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, \
    HabitDestroyAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('', HabitListAPIView.as_view(), name='habit_list'),
    path('<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_detail'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_change'),
    path('delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_delete'),
    ]
