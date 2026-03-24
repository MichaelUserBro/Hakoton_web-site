from django.contrib import admin
from .models import Event, Participation

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'points', 'event_type')
    list_filter = ('event_type', 'date')
    search_fields = ('title', 'location')

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    # Используем правильное имя поля: is_confirmed
    list_display = ('user', 'event', 'is_confirmed', 'registered_at')
    list_filter = ('is_confirmed', 'event')
    search_fields = ('user__username', 'event__title')