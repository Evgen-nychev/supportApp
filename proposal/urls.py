from django.conf.urls import url
from .views import add, list, detail, long_polling, detail_edit

urlpatterns = [
    url(r'^add/$', add),
    url(r'^list/$', list),
    url(r'^detail/(?P<id>\d+)/$', detail),
    url(r'^detail/(?P<id>\d+)/edit/$', detail_edit),
    url(r'^polling/(?P<id>\d+)/$', long_polling)
]
