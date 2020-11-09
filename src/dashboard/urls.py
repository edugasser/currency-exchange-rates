# encoding: utf-8
from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.DashboardView.as_view(), name='dashboard'),
]
