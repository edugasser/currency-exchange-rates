import urllib
from datetime import timedelta, date

from rest_framework.test import APITestCase

from src.currency_exchange.constants import TypeProvider
from src.currency_exchange.models import Currency, CurrencyExchangeRate, \
    Provider


class CurrencyExchangeRateTestCase(APITestCase):
    url = "/api/currency-rates/?{}"

    def setUp(self):
        Provider.objects.create(provider=TypeProvider.MOCK, default=True)
        euro = Currency.objects.create(code="EUR", name="Euro", symbol="€")
        usd = Currency.objects.create(code="USD", name="Dollar", symbol="$")
        self.today = date.today()
        self.yesterday = self.today - timedelta(days=1)

        CurrencyExchangeRate.objects.create(
            source_currency=euro,
            exchanged_currency=usd,
            valuation_date=self.today,
            rate_value=1.30
        )
        CurrencyExchangeRate.objects.create(
            source_currency=usd,
            exchanged_currency=euro,
            valuation_date=self.yesterday,
            rate_value=0.4
        )

    def test_retrieve_wrong_parameters(self):
        # Given
        response = self.client.get(self.url.format(""))
        data = response.json()
        expected = ['Required params: date_from and date_to']

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, expected)

    def test_retrieve_currency_exchanges(self):
        # Given
        params = urllib.parse.urlencode(
            {
                "date_from": self.yesterday.strftime("%Y-%m-%d"),
                "date_to": self.today.strftime("%Y-%m-%d")
            }
        )

        # When
        response = self.client.get(self.url.format(params))
        data = response.json()

        # Then
        results = 4
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), results)
