from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Главная страница приложения events
    path('', views.event_list, name='event_list'),
]