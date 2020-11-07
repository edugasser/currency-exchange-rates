from django.urls import path
from rest_framework import routers

from src.api import views

router = routers.DefaultRouter()

# Define routes
urlpatterns = [
    path('currency-rates/', views.CurrencyExchangeRateView.as_view(), name='currency-rates'),  # noqa
    path('convert-currency/<str:origin>/<str:target>/', views.ConvertCurrencyView.as_view(), name='convert-currency')  # noqa
]
