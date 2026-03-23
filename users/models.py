from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('organizer', 'Организатор'),
        ('participant', 'Участник'),
        ('observer', 'Наблюдатель'),
    )
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='participant',
        verbose_name="Роль"
    )
    points = models.PositiveIntegerField(
        default=0, 
        verbose_name="Баллы рейтинга"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"