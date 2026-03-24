from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/join/', views.join_event, name='join_event'),
    path('create/', views.event_create, name='event_create'),
    path('participation/<int:pk>/confirm/', views.confirm_participation, name='confirm_participation'),
]
