from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # 1. Добавили 'event_type' в список полей
        fields = ['title', 'description', 'location', 'date', 'reward_points', 'event_type']
        
        # 2. Настроили виджеты с Bootstrap-классами
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Название мероприятия'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Описание...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Место проведения'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'
            }),
            'reward_points': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество баллов'
            }),
            # Виджет для выбора типа (выпадающий список)
            'event_type': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

        # 3. Добавили понятные названия для полей (labels)
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'location': 'Место проведения',
            'date': 'Дата и время',
            'reward_points': 'Баллы',
            'event_type': 'Тип мероприятия',
        }