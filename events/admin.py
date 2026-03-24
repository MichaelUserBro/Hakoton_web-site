from django.contrib import admin
from .models import Event, Participation

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # Добавили 'event_type' для наглядности в общем списке
    list_display = ('title', 'event_type', 'date', 'reward_points', 'is_active')
    # Фильтры по категории и статусу активности
    list_filter = ('event_type', 'is_active', 'date')
    # Поиск по названию мероприятия
    search_fields = ('title', 'description')
    # Сортировка по дате (ближайшие сверху)
    ordering = ('-date',)

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    # ЗАМЕНЕНО: Используем 'is_confirmed' вместо старого 'status'
    list_display = ('user', 'event', 'is_confirmed', 'registered_at')
    # Фильтр: теперь можно быстро найти всех подтвержденных или участников конкретных типов IT/Медиа
    list_filter = ('is_confirmed', 'event__event_type', 'registered_at')
    # Поиск по логину студента или названию ивента
    search_fields = ('user__username', 'event__title')
    # Возможность быстро подтверждать участников прямо из списка
    list_editable = ('is_confirmed',)