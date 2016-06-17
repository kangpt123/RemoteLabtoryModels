from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^labinfos/$', views.labinfos, name='labinfos'),
    url(r'^timeselect/$', views.timeSelect, name='timeselect'),
]
