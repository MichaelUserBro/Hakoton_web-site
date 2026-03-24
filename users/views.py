from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy

from .models import User
from .forms import MyUserCreationForm
from events.models import Participation 
from django.utils import timezone  

# 1. Регистрация
class SignUpView(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login') 
    template_name = 'registration/register.html'


@login_required
def profile_view(request):
    user = request.user
    
    if user.role == 'organizer':
        # Используем твой related_name 'created_events'
        all_organized = user.created_events.all()
        
        # Считаем и фильтруем
        past_events = all_organized.filter(date__lt=timezone.now())
        future_events = all_organized.filter(date__gte=timezone.now())
        
        context = {
            'user': user,
            'past_count': past_events.count(),
            'future_count': future_events.count(),
            # Можно также передать сами списки, если захочешь их вывести позже
            'participations': None, 
        }
    else:
        # Логика для студента
        user_participations = Participation.objects.filter(user=user).select_related('event')
        context = {
            'user': user,
            'participations': user_participations,
        }
    
    return render(request, 'users/profile.html', context)

# 3. Рейтинг (Только для студентов)
def leaderboard_view(request):
    try:
        # Исключаем организаторов из рейтинга и берем топ-100 по баллам
        users_top = User.objects.exclude(role='organizer').order_by('-points')[:100]
    except Exception:
        # Если поля points еще нет в БД, просто исключаем организаторов
        users_top = User.objects.exclude(role='organizer')[:100]
    
    return render(request, 'users/leaderboard.html', {'users_top': users_top})