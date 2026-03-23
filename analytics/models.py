from django.db import models
from django.conf import settings

class PointHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='point_history',
        verbose_name="Пользователь"
    )
    event = models.ForeignKey(
        'events.Event', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Мероприятие"
    )
    amount = models.IntegerField(verbose_name="Количество баллов")
    description = models.CharField(max_length=255, verbose_name="Описание операции")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата начисления")

    class Meta:
        verbose_name = "История баллов"
        verbose_name_plural = "История баллов"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.amount} за {self.description}"