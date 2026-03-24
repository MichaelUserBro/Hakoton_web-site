from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('participant', 'Участник'),
        ('organizer', 'Организатор'),
        ('inspector', 'Инспектор'),

        
    )

    # Роль пользователя
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='participant',
        verbose_name="Роль"
    )

    # Основные баллы (общие)
    points = models.PositiveIntegerField(default=0, verbose_name="Баллы рейтинга")
    
    # Баллы по категориям (для Задача №3 и Инспектора)
    points_it = models.PositiveIntegerField(default=0, verbose_name="Баллы: IT")
    points_social = models.PositiveIntegerField(default=0, verbose_name="Баллы: Социальное")
    points_project = models.PositiveIntegerField(default=0, verbose_name="Баллы: Проекты")
    points_media = models.PositiveIntegerField(default=0, verbose_name="Баллы: Медиа")
        
    # Дополнительная информация
    city = models.CharField(max_length=100, blank=True, verbose_name="Город")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    direction = models.CharField(max_length=100, blank=True, null=True, verbose_name="Направление деятельности")
    
    # Для организаторов
    trust_rating = models.FloatField(default=5.0, verbose_name="Рейтинг доверия")

    usual_rewards = models.TextField(blank=True, verbose_name="Типичные призы")
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"