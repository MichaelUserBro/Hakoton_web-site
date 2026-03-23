from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    # Мы берем пользователя прямо из запроса (request.user)
    # Благодаря @login_required, мы уверены, что пользователь вошел в систему
    return render(request, 'users/profile.html', {'user': request.user})