from django.shortcuts import render
from .models import Event

def event_list(request):
    # Получаем только активные мероприятия, сортируем по дате (ближайшие сверху)
    events = Event.objects.filter(is_active=True).order_by('date')
    return render(request, 'events/event_list.html', {'events': events})