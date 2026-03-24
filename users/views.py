from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone 

from .models import User
from .forms import MyUserCreationForm
from events.models import Participation 

# 1. Регистрация
class SignUpView(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login') 
    template_name = 'registration/register.html'

# 2. Профиль (с детальной статистикой)
@login_required
def profile_view(request):
    user = request.user
    
    if user.role == 'organizer':
        all_organized = user.created_events.all()
        past_events = all_organized.filter(date__lt=timezone.now())
        future_events = all_organized.filter(date__gte=timezone.now())
        
        context = {
            'user': user,
            'past_count': past_events.count(),
            'future_count': future_events.count(),
        }
    else:
        # Для студента подгружаем его записи на мероприятия
        user_participations = Participation.objects.filter(user=user).select_related('event')
        context = {
            'user': user,
            'participations': user_participations,
        }
    
    return render(request, 'users/profile.html', context)

# 3. Обновленный Рейтинг (6 столбцов: имя, 4 категории, сумма)
def leaderboard_view(request):
    # Фильтруем только участников (студентов)
    # Сортируем по убыванию общей суммы баллов (поле 'points')
    users_top = User.objects.filter(role='participant').order_by('-points')[:100]
    
    return render(request, 'users/leaderboard.html', {'users_top': users_top})