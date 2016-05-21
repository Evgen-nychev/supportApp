from django.conf.urls import url
from .views import add, list, detail, message_add

urlpatterns = [
    url(r'^add/$', add),
    url(r'^list/$', list),
    url(r'^detail/(?P<id>\d+)/$', detail),
    url(r'^message/add/$', message_add)
]
