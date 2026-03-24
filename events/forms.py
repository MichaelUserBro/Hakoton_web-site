from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # Убедись, что в models.py поле называется 'points'. 
        # Если там 'reward_points', просто переименуй 'points' обратно ниже.
        fields = ['title', 'description', 'location', 'date', 'points', 'event_type']
        
        # Список полей, которые будут доступны в форме
        fields = ['title', 'description', 'location', 'date', 'reward_points', 'event_type']
        
        # Настройка виджетов для соответствия стилям Bootstrap 5
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Название мероприятия'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Подробное описание мероприятия...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Место проведения (аудитория, адрес или ссылка)'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 100'
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

        # Человекочитаемые названия для полей
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'location': 'Место проведения',
            'date': 'Дата и время',
            'points': 'Баллы',
            'event_type': 'Тип мероприятия',
            'reward_points': 'Количество баллов',
            'event_type': 'Категория мероприятия',
        }