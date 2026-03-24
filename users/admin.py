from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Добавляем наши поля (role и points) в список отображения
    list_display = ('username', 'email', 'role', 'points', 'is_staff')
    # Добавляем возможность редактировать эти поля в самой админке
    fieldsets = UserAdmin.fieldsets + (
        ('Доп. информация', {
            'fields': ('role', 'points', 'trust_rating', 'usual_rewards')
        }),
        ('Баллы по категориям', {
            'fields': ('points_it', 'points_social', 'points_project', 'points_media')
        }),
    )