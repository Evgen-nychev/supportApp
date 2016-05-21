from django.conf.urls import url, include
from .views import login, logout, check

urlpatterns = [
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^check/$', check)
]