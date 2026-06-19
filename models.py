from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Менеджер для кастомної моделі користувача, де email є унікальним ідентифікатором
    для автентифікації замість стандартного username.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email є обов\'язковим полем')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Хешування пароля
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser повинен мати is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser повинен мати is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Кастомна модель користувача.
    """
    GENDER_CHOICES = [
        ('M', 'Чоловіча'),
        ('F', 'Жіноча'),
        ('O', 'Інша'),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Task(models.Model):
    """
    Модель для зберігання завдань користувача (To-Do List).
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title