from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^taskslisting/$', views.tasks_listing, name='tasks-list'),
]
