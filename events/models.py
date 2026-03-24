from django.db import models
from django.conf import settings

class Event(models.Model):
    # Список категорий для Задача №3
    EVENT_TYPES = [
        ('it', 'IT'),
        ('social', 'Социальное'),
        ('project', 'Проектная деятельность'),
        ('media', 'Медиа'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название мероприятия")
    description = models.TextField(verbose_name="Описание")
    date = models.DateTimeField(verbose_name="Дата и время проведения")
    location = models.CharField(max_length=255, verbose_name="Место проведения")
    reward_points = models.PositiveIntegerField(default=10, verbose_name="Баллы за участие")
    
    # Новое поле: Тип мероприятия
    event_type = models.CharField(
        max_length=20, 
        choices=EVENT_TYPES, 
        default='it', 
        verbose_name="Тип мероприятия"
    )
    
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events',
        verbose_name="Организатор"
    )
    
    bonus_info = models.CharField(max_length=255, blank=True, verbose_name="Дополнительные бонусы (мерч и т.д.)")
    is_active = models.BooleanField(default=True, verbose_name="Актуально")

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return self.title

class Participation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Участник")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Мероприятие")
    # Переименовал в is_confirmed для соответствия шаблонам
    is_confirmed = models.BooleanField(default=False, verbose_name="Присутствие подтверждено")
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        unique_together = ('user', 'event')
        verbose_name = "Запись на мероприятие"
        verbose_name_plural = "Записи на мероприятия"

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"