from django.shortcuts import render, get_object_or_404
from .models import Event

def event_list(request):
    # Получаем только активные мероприятия, сортируем по дате (ближайшие сверху)
    events = Event.objects.filter(is_active=True).order_by('date')
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    # Находим событие по первичному ключу (pk) или выдаем 404, если его нет
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Participation

@login_required # Только залогиненный пользователь может записаться
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Создаем запись об участии, если её еще нет (get_or_create защищает от дублей)
    Participation.objects.get_or_create(user=request.user, event=event)
    
    # После записи возвращаем пользователя на страницу этого мероприятия
    return redirect('events:event_detail', pk=pk)