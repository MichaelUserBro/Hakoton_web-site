from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone 
from django.db.models import Count, Avg, Q
from django.utils.timezone import now
from django.contrib.auth.decorators import user_passes_test

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
# 2. Личный кабинет
@login_required
def profile_view(request):
    user_participations = Participation.objects.filter(user=request.user).select_related('event')
    return render(request, 'users/profile.html', {
        'user': request.user,
        'participations': user_participations,
    })

# 3. Обновленный Рейтинг (6 столбцов: имя, 4 категории, сумма)
def leaderboard_view(request):
    # Фильтруем только участников (студентов)
    # Сортируем по убыванию общей суммы баллов (поле 'points')
    users_top = User.objects.filter(role='participant').order_by('-points')[:100]
    def leaderboard_view(request):
    # Оставляем только эту строку: фильтруем участников и сортируем
        users_top = User.objects.filter(role='participant').order_by('-points')[:100]
    
        return render(request, 'users/leaderboard.html', {'users_top': users_top})
    return render(request, 'users/leaderboard.html', {'users_top': users_top})

# --- БЛОК ИНСПЕКТОРА ---

def is_hr(user):
    return user.is_staff or user.is_superuser

# 1. Функция проверки прав: пускаем только тех, у кого роль 'inspector'
def is_inspector(user):
    return user.is_authenticated and (user.role == 'inspector' or user.is_superuser)

from django.db.models import Count, Avg, Q

@user_passes_test(is_inspector)
def hr_inspector_view(request):
    candidates = User.objects.annotate(
        events_count=Count(
            'participation', 
            # ИСПРАВЛЕНО: is_confirmed вместо status
            filter=Q(participation__is_confirmed=True) 
        ),
        avg_score=Avg(
            # ИСПРАВЛЕНО: points вместо reward_points
            'participation__event__points', 
            filter=Q(participation__is_confirmed=True)
        )
    ).distinct()

    # --- Код фильтров (город, возраст и т.д.) остается без изменений ---
    city_query = request.GET.get('city')
    min_age = request.GET.get('min_age')
    min_events = request.GET.get('min_events')
    sort_by = request.GET.get('sort', '-avg_score')

    if city_query:
        candidates = candidates.filter(city__icontains=city_query)
    
    if min_events:
        candidates = candidates.filter(events_count__gte=min_events)

    if min_age:
        try:
            current_year = now().year
            birth_year_limit = current_year - int(min_age)
            candidates = candidates.filter(birth_date__year__lte=birth_year_limit)
        except (ValueError, TypeError):
            pass

    return render(request, 'users/hr_inspector.html', {
        'candidates': candidates.order_by(sort_by),
    })

    # Дальше фильтры остаются как были...
    city_query = request.GET.get('city')
    min_age = request.GET.get('min_age')
    min_events = request.GET.get('min_events')
    sort_by = request.GET.get('sort', '-avg_score')

    if city_query:
        candidates = candidates.filter(city__icontains=city_query)
    
    if min_events:
        candidates = candidates.filter(events_count__gte=min_events)

    if min_age:
        try:
            current_year = now().year
            birth_year_limit = current_year - int(min_age)
            candidates = candidates.filter(birth_date__year__lte=birth_year_limit)
        except (ValueError, TypeError):
            pass

    return render(request, 'users/hr_inspector.html', {
        'candidates': candidates.order_by(sort_by),
    })