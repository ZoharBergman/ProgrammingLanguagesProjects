from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView, name='home'),
    url(r'^(?P<user_id>[0-9]+)/$', views.MessageView, name='message'),
]