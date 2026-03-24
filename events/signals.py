from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Participation
from django.db import transaction

@receiver(post_save, sender=Participation)
def update_user_points(sender, instance, created, **kwargs):
    """
    Сигнал срабатывает при сохранении участия.
    Если is_confirmed = True, начисляем баллы в общую сумму и в нужную категорию.
    """
    # 1. Проверяем новое поле is_confirmed (вместо старого status)
    if instance.is_confirmed:
        user = instance.user
        event = instance.event
        points_to_add = event.points

        # Используем atomic, чтобы данные сохранились корректно
        with transaction.atomic():
            # 2. Начисляем в общую сумму
            user.points += points_to_add

            # 3. Распределяем по категориям (Задача №2)
            if event.event_type == 'it':
                user.points_it += points_to_add
            elif event.event_type == 'social':
                user.points_social += points_to_add
            elif event.event_type == 'project':
                user.points_project += points_to_add
            elif event.event_type == 'media':
                user.points_media += points_to_add

            # Сохраняем обновленные данные пользователя
            user.save()