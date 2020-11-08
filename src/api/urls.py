from django.urls import path
from rest_framework import routers

from src.api import views

router = routers.DefaultRouter()


urlpatterns = [
    path(
        'currency-rates/<str:origin>/',
        views.ListCurrencyExchangeRateView.as_view(),
        name='currency-rates'
    ),
    path(
        'convert-currency/<str:origin>/<str:target>/',
        views.ConvertCurrencyView.as_view(),
        name='convert-currency'
    ),
    path(
        'twr/<str:origin>/<str:target>/<str:date_invested>/',
        views.TimeWeightedRateView.as_view(),
        name='retrieve-twr'
    )
]
