from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Варианты ролей согласно твоему запросу
    ROLE_CHOICES = (
        ('participant', 'Участник'),
        ('organizer', 'Организатор'),
        ('inspector', 'Инспектор'),
    )
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='participant',
        verbose_name="Роль"
    )
    
    # Баллы для участников
    points = models.PositiveIntegerField(
        default=0, 
        verbose_name="Баллы рейтинга"
    )
    
    # Направление (например: Проектирование, Медиа)
    direction = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Направление деятельности"
    )

    # Рейтинг доверия для организаторов (от 0.0 до 5.0)
    trust_rating = models.FloatField(
        default=5.0, 
        verbose_name="Рейтинг доверия"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"