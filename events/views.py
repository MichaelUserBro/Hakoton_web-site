from django.shortcuts import render, get_object_or_404
from .models import Event
from django.contrib import messages

def event_list(request):
    # Получаем только активные мероприятия, сортируем по дате (ближайшие сверху)
    events = Event.objects.filter(is_active=True).order_by('date')
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    participation = None
    is_joined = False

    if request.user.is_authenticated:
        # Пытаемся найти запись пользователя на это событие
        participation = Participation.objects.filter(user=request.user, event=event).first()
        is_joined = participation is not None

    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_joined': is_joined,
        'participation': participation  # Передаем объект участия в шаблон
    })

from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Participation

# 1. Список всех мероприятий
def event_list(request):
    # Убираем filter(is_active=True) на время теста, чтобы точно увидеть все события из базы
    events = Event.objects.all().order_by('date')
    return render(request, 'events/event_list.html', {'events': events})

# 2. Детальная страница мероприятия
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

# 3. Логика записи на мероприятие
@login_required
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    participation, created = Participation.objects.get_or_create(user=request.user, event=event)
    
    if created:
        # 2. Добавляем зеленое уведомление об успехе
        messages.success(request, f'Вы успешно записаны на мероприятие "{event.title}"!')
    else:
        # 3. Добавляем желтое уведомление, если человек уже нажал кнопку второй раз
        messages.info(request, 'Вы уже записаны на это мероприятие.')
    
    return redirect('events:event_detail', pk=pk)
    # Создаем запись об участии
    Participation.objects.get_or_create(user=request.user, event=event)
    return redirect('events:event_detail', pk=pk)
