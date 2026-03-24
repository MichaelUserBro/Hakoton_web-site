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
    # Создаем запись об участии
    Participation.objects.get_or_create(user=request.user, event=event)
    return redirect('events:event_detail', pk=pk)