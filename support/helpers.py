#Проверка авторизации
def cheсk_login(request):
    if request.user.is_authenticated():
        return request.user
    else:
        return False
