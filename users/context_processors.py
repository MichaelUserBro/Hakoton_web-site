def user_points(request):
    # Если пользователь вошел в систему, отдаем его баллы
    if request.user.is_authenticated:
        return {'current_user_points': request.user.points}
    # Если не вошел — отдаем 0
    return {'current_user_points': 0}