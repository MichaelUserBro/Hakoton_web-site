from django.contrib import admin
from django.urls import path, include # Импортируй include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),   # Подключаем твои пути
    path('events/', include('events.urls')), # Подключаем пути коллеги
]