from datetime import timedelta, date

from rest_framework.test import APITestCase

from src.currency_exchange.models import Currency, CurrencyExchangeRate


class RetrieveTwrTestCase(APITestCase):
    url = "/api/v1/twr/{origin}/{target}/{date_invested}/?amount={amount}"

    def setUp(self):
        euro = Currency.objects.create(code="EUR", name="Euro", symbol="€")
        usd = Currency.objects.create(code="USD", name="Dollar", symbol="$")
        self.today = date.today()
        self.yesterday = self.today - timedelta(days=1)

        CurrencyExchangeRate.objects.create(
            source_currency=euro,
            exchanged_currency=usd,
            valuation_date=self.yesterday,
            rate_value=0.40
        )
        CurrencyExchangeRate.objects.create(
            source_currency=euro,
            exchanged_currency=usd,
            valuation_date=self.today,
            rate_value=1.30
        )

    def test_retrieve(self):
        # Given
        endpoint = self.url.format(
            origin="EUR",
            target="USD",
            amount="50",
            date_invested=self.yesterday.strftime("%Y-%m-%d")
        )
        response = self.client.get(endpoint)
        data = response.json()

        expected = {
            'origin_currency': 'EUR',
            'target_currency': 'USD',
            'amount': '50.000000',
            'twr': '225.000000',
            'date_invested': self.yesterday.strftime("%Y-%m-%d")
        }

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected)

    def test_retrieve_wrong_parameters(self):
        # Given
        endpoint = self.url.format(
            origin="EUR",
            target="USD",
            amount="asdf",
            date_invested="2020-01-01"
        )
        response = self.client.get(endpoint)
        data = response.json()
        expected = {
            'amount': ['A valid number is required.']
        }

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, expected)
