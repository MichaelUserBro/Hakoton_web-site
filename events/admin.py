from django.contrib import admin
from .models import Event, Participation

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'points_award', 'organizer', 'is_active')
    list_filter = ('date', 'is_active')
    search_fields = ('title', 'description')

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'registered_at')
    list_filter = ('status', 'event')