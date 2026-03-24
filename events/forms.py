from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # Убедись, что в models.py поле называется 'points'. 
        # Если там 'reward_points', просто переименуй 'points' обратно ниже.
        fields = ['title', 'description', 'location', 'date', 'points', 'event_type']
        
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
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество баллов'
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

        labels = {
            'title': 'Название',
            'description': 'Описание',
            'location': 'Место проведения',
            'date': 'Дата и время',
            'points': 'Баллы',
            'event_type': 'Тип мероприятия',
        }