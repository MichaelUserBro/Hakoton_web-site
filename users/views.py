from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone 
from django.db.models import Count, Avg, Q
from django.utils.timezone import now
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import get_object_or_404, redirect
from .models import Review

from .models import User
from .forms import MyUserCreationForm
from events.models import Participation 

# 1. Регистрация
class SignUpView(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login') 
    template_name = 'registration/register.html'

# 2. Профиль (с расчетом места и прогресса до ТОП-100)
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
        # --- НОВАЯ ЛОГИКА РЕЙТИНГА ---
        # Получаем всех участников, отсортированных по баллам
        all_participants = User.objects.filter(role='participant').order_by('-points', 'username')
        participants_list = list(all_participants.values_list('id', flat=True))
        
        # 1. Текущее место (индекс в списке + 1)
        try:
            current_rank = participants_list.index(user.id) + 1
        except ValueError:
            current_rank = len(participants_list)
            
        # 2. Расчет баллов до ТОП-100
        top_100 = all_participants[:100]
        if all_participants.count() >= 100:
            # Берем баллы 100-го человека
            threshold_points = list(top_100)[99].points
        else:
            # Если участников меньше 100, порогом будет последний человек в списке
            threshold_points = all_participants.last().points if all_participants.exists() else 0
            
        # Сколько не хватает баллов
        points_to_top = max(0, threshold_points - user.points)
        
        # Процент для прогресс-бара
        if threshold_points > 0 and user.points < threshold_points:
            progress_percent = int((user.points / threshold_points) * 100)
        else:
            progress_percent = 100 # Если уже в топе или порог 0
            
        user_participations = Participation.objects.filter(user=user).select_related('event')
        
        context = {
            'user': user,
            'participations': user_participations,
            'current_rank': current_rank,
            'points_to_top': points_to_top,
            'progress_percent': progress_percent,
            'threshold_points': threshold_points,
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
# 3. Обновленный Рейтинг (фильтрация по направлениям)
def leaderboard_view(request):
    # Базовый запрос: только участники (студенты)
    participants = User.objects.filter(role='participant')

    # Формируем 5 разных списков для разных вкладок
    context = {
        # Общий топ по всем баллам
        'users_top': participants.order_by('-points')[:100],
        
        # Топ IT (поле points_it)
        'users_it': participants.order_by('-points_it')[:100],
        
        # Топ Социальное (поле points_social)
        'users_social': participants.order_by('-points_social')[:100],
        
        # Топ Проекты (поле points_project)
        'users_project': participants.order_by('-points_project')[:100],
        
        # Топ Медиа (поле points_media)
        'users_media': participants.order_by('-points_media')[:100],
    }
    
    return render(request, 'users/leaderboard.html', context)

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


def organizers_list_view(request):
    # Фильтруем только тех, у кого роль 'organizer'
    organizers = User.objects.filter(role='organizer')
    return render(request, 'users/organizers_list.html', {'organizers': organizers})


def organizer_detail_view(request, pk):
    organizer = get_object_or_404(User, pk=pk, role='organizer')
    reviews = organizer.reviews.all().order_by('-created_at')
    
    if request.method == 'POST':
        # Простая обработка формы без создания отдельного класса Form
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        if text and rating:
            Review.objects.create(
                organizer=organizer,
                author=request.user,
                text=text,
                rating=int(rating)
            )
            return redirect('users:organizer_detail', pk=pk)

    return render(request, 'users/organizer_detail.html', {
        'organizer': organizer,
        'reviews': reviews
    })
    users_top = User.objects.filter(role='participant').order_by('-points')[:100]
    return render(request, 'users/leaderboard.html', {'users_top': users_top})
