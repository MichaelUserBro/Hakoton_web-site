from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy

from .models import User
from .forms import MyUserCreationForm
from events.models import Participation  # Импорт для отображения записей на ивенты

# 1. Регистрация
class SignUpView(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login') 
    template_name = 'registration/register.html'

# 2. Личный кабинет (объединенная версия)
@login_required
def profile_view(request):
    # Достаем записи об участии этого пользователя вместе с данными о мероприятиях
    user_participations = Participation.objects.filter(user=request.user).select_related('event')
    
    context = {
        'user': request.user,
        'participations': user_participations,
    }
    return render(request, 'users/profile.html', context)

# 3. Рейтинг
def leaderboard_view(request):
    try:
        # Пытаемся отсортировать по баллам, если поле points существует
        users_top = User.objects.all().order_by('-points')[:100]
    except Exception:
        # Если поля points еще нет в БД (не прошли миграции), берем просто список
        users_top = User.objects.all()[:100]
    
    return render(request, 'users/leaderboard.html', {'users_top': users_top})