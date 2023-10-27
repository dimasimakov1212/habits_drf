from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """ Задаем права владельцев объектов """
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True

        return False


class IsSubscriber(BasePermission):
    """
    Задаем права подписчиков
    """
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True

        return False
