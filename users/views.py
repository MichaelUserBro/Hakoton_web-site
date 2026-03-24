from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User  # Оставляем, если он нужен для других функций
from events.models import Participation  # Импорт модели участий

@login_required
def profile_view(request):
    # Достаем все записи об участии конкретно этого пользователя
    user_participations = Participation.objects.filter(user=request.user).select_related('event')
    
    return render(request, 'users/profile.html', {
        'participations': user_participations,
        'user': request.user  # Добавляем юзера на всякий случай
    })

def leaderboard_view(request):
    # Твоя функция лидерборда остается без изменений
    users_top = User.objects.all().order_by('-points')[:100]
    return render(request, 'users/leaderboard.html', {'users_top': users_top})