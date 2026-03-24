from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Participation
from .forms import EventForm

# 1. Список всех мероприятий
def event_list(request):
    # Оставляем .all() для тестов, чтобы видеть все созданные события
    events = Event.objects.all().order_by('date')
    return render(request, 'events/event_list.html', {'events': events})

# 2. Детальная страница мероприятия
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    participation = None
    is_joined = False

    if request.user.is_authenticated:
        # Проверяем, записан ли текущий пользователь
        participation = Participation.objects.filter(user=request.user, event=event).first()
        is_joined = participation is not None

    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_joined': is_joined,
        'participation': participation
    })

# 3. Логика записи на мероприятие
@login_required
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # get_or_create сразу проверяет, есть ли запись, и если нет — создает её
    participation, created = Participation.objects.get_or_create(user=request.user, event=event)
    
    if created:
        messages.success(request, f'Вы успешно записаны на мероприятие "{event.title}"!')
    else:
        messages.info(request, 'Вы уже записаны на это мероприятие.')
    
    return redirect('events:event_detail', pk=pk)


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Назначаем текущего пользователя организатором
            event.save()
            messages.success(request, 'Мероприятие успешно создано!')
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm()
    
    return render(request, 'events/event_form.html', {'form': form})