from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('', include('users.urls')), # Проверь, чтобы тут НЕ БЫЛО namespace='users', если ты уже написал app_name в самом приложении
    path('accounts/', include('django.contrib.auth.urls')),
]