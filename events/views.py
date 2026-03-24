from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Participation
from .forms import EventForm

# 1. Список всех мероприятий
def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events/event_list.html', {'events': events})

# 2. Детальная страница мероприятия
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    all_participations = Participation.objects.filter(event=event).select_related('user')
    
    is_joined = False
    user_participation = None

    if request.user.is_authenticated:
        user_participation = all_participations.filter(user=request.user).first()
        is_joined = user_participation is not None

    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_joined': is_joined,
        'user_participation': user_participation,
        'all_participations': all_participations 
    })

# 3. Логика записи на мероприятие
@login_required
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    participation, created = Participation.objects.get_or_create(user=request.user, event=event)
    
    if created:
        messages.success(request, f'Вы успешно записаны на мероприятие "{event.title}"!')
    else:
        messages.info(request, 'Вы уже записаны на это мероприятие.')
    
    return redirect('events:event_detail', pk=pk)

# 4. Создание мероприятия
@login_required
def event_create(request):
    if request.user.role != 'organizer':
        messages.error(request, "Только организаторы могут создавать мероприятия.")
        return redirect('events:event_list')

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Мероприятие успешно создано!')
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm()
    
    return render(request, 'events/event_form.html', {'form': form})

# 5. ПОДТВЕРЖДЕНИЕ УЧАСТИЯ И НАЧИСЛЕНИЕ БАЛЛОВ (Новое!)
# ... (начало файла без изменений до функции confirm_participation)

# ШАГ 2: РЕДАКТИРОВАНИЕ МЕРОПРИЯТИЯ (Добавлено!)
@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Проверка прав: только организатор этого события
    if event.organizer != request.user:
        messages.error(request, "Вы не можете редактировать чужое мероприятие.")
        return redirect('events:event_detail', pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения сохранены!')
            return redirect('events:event_detail', pk=pk)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_edit.html', {'form': form, 'event': event})

# 5. ПОДТВЕРЖДЕНИЕ УЧАСТИЯ (Исправлено, чтобы не было дублей баллов!)
@login_required
def confirm_participation(request, pk):
    participation = get_object_or_404(Participation, pk=pk)
    
    if request.user != participation.event.organizer:
        messages.error(request, "У вас нет прав для этого действия.")
        return redirect('events:event_detail', pk=participation.event.pk)

    if not participation.is_confirmed:
        participation.is_confirmed = True
        participation.save()

        user = participation.user
        event = participation.event
        # ИСПРАВЛЕНО: используем points вместо reward_points
        pts = event.points 

        # Общий счетчик
        user.points += pts

        # Категориальные счетчики (Убедись, что эти поля есть в users/models.py!)
        if event.event_type == 'it':
            user.points_it += pts
        elif event.event_type == 'social':
            user.points_social += pts
        elif event.event_type == 'project':
            user.points_project += pts
        elif event.event_type == 'media':
            user.points_media += pts
        
        user.save()
        messages.success(request, f"Участие {user.username} подтверждено. Баллы начислены!")
        # МЫ УДАЛИЛИ ОТСЮДА РУЧНОЕ НАЧИСЛЕНИЕ БАЛЛОВ.
        # Теперь они начисляются ТОЛЬКО через сигнал в models.py.
        participation.save() 
        messages.success(request, f"Участие {participation.user.username} подтверждено!")
    
    return redirect('events:event_detail', pk=participation.event.pk)