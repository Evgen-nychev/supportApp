from django.conf.urls import url
from .views import add, list, detail, message_add, detail_edit

urlpatterns = [
    url(r'^add/$', add),
    url(r'^list/$', list),
    url(r'^detail/(?P<id>\d+)/$', detail),
    url(r'^detail/(?P<id>\d+)/edit/$', detail_edit),
    url(r'^message/add/$', message_add)
]
