from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Сюда коллега будет добавлять список мероприятий
    path('', views.events_list, name='events_list'),
]