from django.conf.urls import url
from django.contrib import admin

from index import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^flag/$', views.flag),
    url(r'^ctf_finish/$', views.ctf_finish)
]
