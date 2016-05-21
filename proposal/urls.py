from django.conf.urls import url
from .views import add

urlpatterns = [
    url(r'^add/$', add)
]
