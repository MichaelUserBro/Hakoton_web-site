from django.contrib import admin
from .models import Event, Participation

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # Добавил 'event_type' в список отображения
    list_display = ('title', 'event_type', 'date', 'reward_points', 'is_active')
    # Добавил фильтр по типу мероприятия
    list_filter = ('event_type', 'is_active', 'date')
    search_fields = ('title', 'description')

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    # ЗАМЕНЕНО: 'status' на 'is_confirmed'
    list_display = ('user', 'event', 'is_confirmed', 'registered_at')
    # Добавлены фильтры для удобства поиска
    list_filter = ('is_confirmed', 'event__event_type')
    search_fields = ('user__username', 'event__title')