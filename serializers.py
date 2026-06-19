from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Task


class UserSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для профілю користувача та реєстрації.
    """
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'gender', 'date_of_birth', 'password')

    def create(self, validated_data):
        # Перевизначення методу create для коректного хешування пароля
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            gender=validated_data.get('gender', ''),
            date_of_birth=validated_data.get('date_of_birth')
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Серіалізатор для автентифікації користувача.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Невірні облікові дані', code='authorization')
        else:
            raise serializers.ValidationError('Необхідно вказати email та пароль', code='authorization')

        data['user'] = user
        return data


class TaskSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для завдань.
    """

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'is_completed', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')