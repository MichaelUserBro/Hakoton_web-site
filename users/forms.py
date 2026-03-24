from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Добавляем поле role, чтобы оно появилось в форме
        fields = ("username", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap-класс для красивого отображения списка
        if 'role' in self.fields:
            self.fields['role'].widget.attrs.update({'class': 'form-select'})