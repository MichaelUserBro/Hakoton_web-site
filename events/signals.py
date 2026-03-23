from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Participation

@receiver(post_save, sender=Participation)
def update_user_points(sender, instance, created, **kwargs):
    """
    Сигнал срабатывает при каждом сохранении записи об участии.
    Если статус 'Присутствие подтверждено' (True), начисляем баллы.
    """
    # Проверяем, что статус стал True
    if instance.status:
        user = instance.user
        # Прибавляем баллы из связанного мероприятия
        user.points += instance.event.points_award
        user.save()