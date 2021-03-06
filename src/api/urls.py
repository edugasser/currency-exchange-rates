from django.urls import re_path
from rest_framework import routers

from src.api.v1 import views

router = routers.DefaultRouter()


urlpatterns = [
    re_path(
        r'^(?P<version>(v1))/historical/'
        r'(?P<origin>[A-Z]+)/'
        r'(?P<start>[0-9]{4}-[0-9]{2}-[0-9]{2})/'
        r'(?P<end>[0-9]{4}-[0-9]{2}-[0-9]{2})/',
        views.ListCurrencyExchangeRateView.as_view(),
        name='currency-rates'
    ),
    re_path(
        r'^(?P<version>(v1))/convert/'
        r'(?P<origin>[A-Z]+)/'
        r'(?P<target>[A-Z]+)/',
        views.ConvertCurrencyView.as_view(),
        name='convert-currency'
    ),
    re_path(
        r'^(?P<version>(v1))/twr/'
        r'(?P<origin>[A-Z]+)/'
        r'(?P<target>[A-Z]+)/'
        r'(?P<date_invested>[0-9]{4}-[0-9]{2}-[0-9]{2})/',
        views.TimeWeightedRateView.as_view(),
        name='retrieve-twr'
    )
]
