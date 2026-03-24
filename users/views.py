from .models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#@login_required
def profile_view(request):
    # Мы берем пользователя прямо из запроса (request.user)
    # Благодаря @login_required, мы уверены, что пользователь вошел в систему
    return render(request, 'users/profile.html', {'user': request.user})


def leaderboard_view(request):
    # .order_by('-points') — сортировка от большего к меньшему
    # [:10] — берем только первых 10 человек
    users_top = User.objects.all().order_by('-points')[:100]
    
    return render(request, 'users/leaderboard.html', {'users_top': users_top})