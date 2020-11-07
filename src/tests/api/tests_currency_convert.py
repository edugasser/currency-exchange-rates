import json
from datetime import datetime, timedelta, date

from rest_framework.test import APITestCase
import urllib
from src.currency_exchange.models import Currency, CurrencyExchangeRate


class CurrencyConvertTestCase(APITestCase):
    url = "/api/convert-currency/{origin}/{target}/?{params}"

    def setUp(self):
        euro = Currency.objects.create(code="EUR", name="Euro", symbol="€")
        usd = Currency.objects.create(code="USD", name="Dollar", symbol="$")
        self.today = date.today()

        CurrencyExchangeRate.objects.create(
            source_currency=euro,
            exchanged_currency=usd,
            valuation_date=self.today,
            rate_value=1.30
        )

    def test_convert_without_amount_parameter(self):
        # Given
        endpoint = self.url.format(
            origin="nothing",
            target="USD",
            params={}
        )

        # When
        response = self.client.get(endpoint)
        data = response.json()
        expected = ["Required GET param 'amount'"]

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, expected)

    def test_convert_with_non_existed_currency(self):
        # Given
        endpoint = self.url.format(
            origin="COP",
            target="USD",
            params=urllib.parse.urlencode({"amount": 100.0})
        )

        # When
        response = self.client.get(endpoint)
        data = response.json()
        expected = ["An error occurred while converting currency: The currency COP doesn't exist"]  # noqa

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, expected)

    def test_convert_correct_parameters(self):
        # Given
        endpoint = self.url.format(
            origin="EUR",
            target="USD",
            params=urllib.parse.urlencode({"amount": 100.0})
        )
        expected = {
            'amount': 100.0,
            'converted_amount': 130.0,
            'origin_currency': 'EUR',
            'target_currency': 'USD'
        }

        # When
        response = self.client.get(endpoint)
        data = response.json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected)
