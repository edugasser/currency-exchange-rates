from datetime import timedelta, date

from rest_framework.test import APITestCase

from src.currency_exchange.constants import TypeProvider
from src.currency_exchange.models import Currency, CurrencyExchangeRate, \
    Provider


class CurrencyExchangeRateTestCase(APITestCase):
    url = "/api/v1/historical/{origin}/{from_date}/{to_date}/"

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
        response = self.client.get(self.url.format(
            origin="EUR",
            from_date="",
            to_date="")
        )

        # Then
        self.assertEqual(response.status_code, 404)

    def test_retrieve_currency_exchanges(self):
        # Given
        today_str = self.today.strftime("%Y-%m-%d")
        yesterday_str = self.yesterday.strftime("%Y-%m-%d")

        # When
        endpoint = self.url.format(
            origin="EUR",
            from_date=yesterday_str,
            to_date=today_str
        )
        response = self.client.get(endpoint)

        data = response.json()

        # Then
        results = 2
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), results)
        self.assertEqual(data[0]["valuation_date"], yesterday_str)
        self.assertEqual(data[1]["valuation_date"], today_str)
