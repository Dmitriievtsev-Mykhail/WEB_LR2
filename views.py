from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import CustomUser, Task
from .serializers import UserSerializer, LoginSerializer, TaskSerializer


class RegisterView(generics.CreateAPIView):
    """
    Ендпоінт для реєстрації нового користувача.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    """
    Ендпоінт для входу в систему та отримання токена автентифікації.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        # is_valid викине помилку 400 Bad Request у разі невірних даних
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Ендпоінт для перегляду та редагування профілю поточного користувача.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Повертає об'єкт користувача, який здійснив запит (за токеном)
        return self.request.user


class AboutAppView(APIView):
    """
    Ендпоінт, що повертає загальну інформацію про додаток.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        data = {
            "app_name": "To-Do List REST API",
            "description": "Серверна частина Web-додатку для створення, редагування, видалення та перегляду завдань.",
            "emblem_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Open_To_Do_List_Icon.svg/1200px-Open_To_Do_List_Icon.svg.png",
            "version": "1.0.0"
        }
        return Response(data, status=status.HTTP_200_OK)


class TaskViewSet(viewsets.ModelViewSet):
    """
    Набір ендпоінтів для операцій над завданнями (Створення, Читання, Оновлення, Видалення).
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Обмеження доступу: користувач бачить лише власні завдання
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # При створенні завдання воно автоматично прив'язується до поточного користувача
        serializer.save(user=self.request.user)