from rest_framework.permissions import BasePermission
from django.utils import timezone
import jwt


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        from users.utils import decodeJWT

        try:
            user = decodeJWT(request.META.get("HTTP_AUTHORIZATION", None))
        except jwt.exceptions.DecodeError:
            return False
        if not user:
            return False
        request.user = user
        if request.user and request.user.is_authenticated:
            from users.models import User

            User.objects.filter(id=request.user.id).update(last_login=timezone.now())
            return True
        return False
