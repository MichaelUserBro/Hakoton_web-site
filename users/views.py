from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# УДАЛИЛИ: from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from .models import User
from .forms import MyUserCreationForm  # ДОБАВИЛИ импорт новой формы

# Регистрация
class SignUpView(generic.CreateView):
    form_class = MyUserCreationForm  # ЗАМЕНИЛИ форму здесь
    success_url = reverse_lazy('login') 
    template_name = 'registration/register.html'

# Личный кабинет
@login_required
def profile_view(request):
    context = {
        'user': request.user,
    }
    return render(request, 'users/profile.html', context)

# Рейтинг
def leaderboard_view(request):
    try:
        # Сортируем по баллам
        users_top = User.objects.all().order_by('-points')[:100]
    except:
        users_top = User.objects.all()[:100]
    
    return render(request, 'users/leaderboard.html', {'users_top': users_top})