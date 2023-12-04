from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    RefreshSerializer,
    UserSerializer,
)
from .utils import get_access_token, get_refresh_token
from .models import User, Jwt
from api.authentication import IsAuthenticatedCustom
from .authentication import Authentication
from rest_framework import status, generics
from django.db import transaction


# test
class SignupAPI(APIView):
    serializer_class = SignupSerializer

    @transaction.atomic()
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop("password2")
        user = User.objects._create_user(**serializer.validated_data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginAPI(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response({"error": "Invalid username or password"}, status="400")

        Jwt.objects.filter(user_id=user.id).delete()

        access = get_access_token({"user_id": user.id})
        refresh = get_refresh_token()

        Jwt.objects.create(
            user_id=user.id,
            access=access,
            refresh=refresh,
        )

        return Response(
            status=status.HTTP_200_OK, data={"access": access, "refresh": refresh}
        )


class LogoutAPI(APIView):
    permission_classes = (IsAuthenticatedCustom,)

    def get(self, request):
        user_id = request.user.id

        Jwt.objects.filter(user_id=user_id).delete()

        request.session.flush()

        return Response("logged out successfully", status=200)


class RefreshAPI(APIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"data": "존재하지 않는 토큰입니다."}, status="400")
        if not Authentication.verify_token(serializer.validated_data["refresh"]):
            return Response({"data": "토큰이 만료되었습니다."})

        access = get_access_token({"user_id": active_jwt.user.id})
        refresh = get_refresh_token()

        # active_jwt.access = access.decode()
        # active_jwt.refresh = refresh.decode()
        active_jwt.access = access
        active_jwt.refresh = refresh
        active_jwt.save()

        return Response({"access": access, "refresh": refresh})
