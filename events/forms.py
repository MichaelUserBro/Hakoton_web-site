from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # Указываем поля, которые пользователь должен заполнить
        fields = ['title', 'description', 'location', 'date', 'reward_points']
        # Добавляем красивые стили Bootstrap для полей
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название мероприятия'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Описание...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Место проведения'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'reward_points': forms.NumberInput(attrs={'class': 'form-control'}),
        }