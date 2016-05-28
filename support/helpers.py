#Проверка авторизации
def cheсk_login(request):
    if request.user.is_authenticated():
        return request.user
    else:
        return False

def check_filtered_item(items ,item, name):
    if len(item):
        items[name] = item