from django.contrib import admin
from .models import Event, Participation

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'reward_points', 'is_active') 

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status')