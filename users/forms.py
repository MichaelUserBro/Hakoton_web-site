from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class MyUserCreationForm(UserCreationForm): # или та форма, которую ты используешь
    birth_date = forms.DateField(
        label="Дата рождения",
        input_formats=['%d.%m.%Y', '%Y-%m-%d'], # Разрешаем оба формата
        widget=forms.DateInput(
            format='%d.%m.%Y',
            attrs={
                'class': 'form-control',
                'placeholder': 'ДД.ММ.ГГГГ', # Подсказка внутри поля
            }
        ),
        help_text="Введите дату в формате: день.месяц.год (например, 13.05.2007)"
    )
    class Meta(UserCreationForm.Meta):
        model = User
        # Добавляем поле role, чтобы оно появилось в форме
        fields = UserCreationForm.Meta.fields + ('birth_date', 'city', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap-класс для красивого отображения списка
        if 'role' in self.fields:
            self.fields['role'].widget.attrs.update({'class': 'form-select'})