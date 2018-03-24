from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'register$', views.register),
    url(r'login$', views.login),
    url(r'qoutes$', views.qoutes),
    url(r'process/qoute$',views.process_qoute),
    url(r'process/favorite$', views.process_favorite),
    url(r'process/remove$', views.process_remove),
    url(r'users/(?P<user_id>\d+)$', views.user),
    url(r'logout$',views.logout),
]