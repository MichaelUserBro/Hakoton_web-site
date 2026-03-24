from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView # Убедись, что этот импорт есть вверху!

urlpatterns = [
    path('admin/', admin.site.urls),
    # Приложение events должно подключать СВОИ пути (events.urls)
    path('events/', include('events.urls')), 
    # Приложение users подключает СВОИ пути (профиль, рейтинг)
    path('', include('users.urls')), 
]