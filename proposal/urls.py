from django.conf.urls import url
from .views import add, list, detail, long_polling, detail_edit, reports

urlpatterns = [
    url(r'^add/$', add),
    url(r'^list/$', list),
    url(r'^list/(?P<status>[A-Za-z]+)/$', list),
    url(r'^reports/$', reports),
    url(r'^detail/(?P<id>\d+)/$', detail),
    url(r'^detail/(?P<id>\d+)/edit/$', detail_edit),
    url(r'^polling/(?P<id>\d+)/$', long_polling)
]
