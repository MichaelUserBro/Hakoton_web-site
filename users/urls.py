from django.urls import path
from . import views

# app_name позволяет нам обращаться к ссылкам как 'users:profile' или 'users:register'
app_name = 'users'

urlpatterns = [
    # Личный кабинет
    path('profile/', views.profile_view, name='profile'),
    
    # Рейтинг (Таблица лидеров)
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    
    # Регистрация
    # .as_view() нужен, так как SignUpView — это класс, а не обычная функция
    path('register/', views.SignUpView.as_view(), name='register'),

    path('inspector/', views.hr_inspector_view, name='hr_inspector'),

    path('organizers/', views.organizers_list_view, name='organizers_list'),

    path('organizer/<int:pk>/', views.organizer_detail_view, name='organizer_detail'),

    path('export-pdf/<int:user_id>/', views.export_pdf_achievements, name='export_pdf'),
]