<<<<<<< HEAD
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
=======
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
>>>>>>> 4227972d5b448fc245a621df5a05ccc66aea373b

# Рейтинг
def leaderboard_view(request):
<<<<<<< HEAD
    # Твоя функция лидерборда остается без изменений
    users_top = User.objects.all().order_by('-points')[:100]
=======
    try:
        # Сортируем по баллам
        users_top = User.objects.all().order_by('-points')[:100]
    except:
        users_top = User.objects.all()[:100]
    
>>>>>>> 4227972d5b448fc245a621df5a05ccc66aea373b
    return render(request, 'users/leaderboard.html', {'users_top': users_top})