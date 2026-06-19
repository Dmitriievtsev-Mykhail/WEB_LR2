from django.contrib import admin
from .models import CustomUser, Task

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Налаштування відображення моделі користувача в адмін-панелі.
    """
    list_display = ('email', 'name', 'gender', 'is_active', 'is_staff')
    search_fields = ('email', 'name')
    ordering = ('email',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Налаштування відображення моделі завдань в адмін-панелі.
    """
    list_display = ('title', 'user', 'is_completed', 'created_at')
    list_filter = ('is_completed', 'created_at')
    search_fields = ('title', 'description')