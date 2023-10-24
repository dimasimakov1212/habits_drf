from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора для модели User
    """

    class Meta:
        model = User
        fields = '__all__'


class AnyUserSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора для модели User при использовании стронним пользователем
    """

    class Meta:
        model = User
        fields = ('id', 'user_email', 'user_city')
