import datetime

from django.test import TestCase
from mock import Mock

from src.currency_exchange.exchange_retriever.exchange_providers.fixer_io import \
    FixerProvider
from src.currency_exchange.exchange_retriever.exchange_response import \
    ExchangeResponse, CurrencyRate
from src.exceptions import ExchangeProviderError


class FixerIoProviderTestCase(TestCase):

    def setUp(self):
        self.provider = FixerProvider()

    def test_get_latest_no_currencies(self):
        with self.assertRaises(ExchangeProviderError):
            self.provider.get_latest([])

    def test_get_latest_with_currencies(self):
        # Given
        mock_response = {
          "success": True,
          "timestamp": 1604731985,
          "base": "EUR",
          "date": "2020-11-07",
          "rates": {
            "USD": 1.187435,
            "EUR": 1.636036,
          }
        }
        request_mock = Mock(return_value=mock_response)
        self.provider.make_request = request_mock

        # When
        response = self.provider.get_latest(["EUR", "USD"])

        # Then
        expected_response = ExchangeResponse(
            success=True,
            exchange_date=datetime.datetime(2020, 11, 7, 0, 0),
            base_currency='EUR',
            rates=[
                CurrencyRate(
                    currency='USD',
                    rate=1.187435
                ),
                CurrencyRate(
                    currency='EUR',
                    rate=1.636036
                )
            ]
        )
        self.assertEqual(expected_response, response)

    def test_get_historical_with_no_currencies(self):
        with self.assertRaises(ExchangeProviderError):
            self.provider.get_historical([], datetime.date.today())

    def test_get_historical_with_currencies(self):
        # Given
        mock_response = {
            "success": True,
            "timestamp": 1604731985,
            "base": "EUR",
            "date": "2020-11-07",
            "rates": {
                "USD": 1.187435,
                "EUR": 1.636036,
            }
        }
        request_mock = Mock(return_value=mock_response)
        self.provider.make_request = request_mock

        # When
        response = self.provider.get_historical(
            ["EUR", "USD"],
            datetime.date.today()
        )

        # Then
        expected_response = ExchangeResponse(
            success=True,
            exchange_date=datetime.datetime(2020, 11, 7, 0, 0),
            base_currency='EUR',
            rates=[
                CurrencyRate(
                    currency='USD',
                    rate=1.187435
                ),
                CurrencyRate(
                    currency='EUR',
                    rate=1.636036
                )
            ]
        )
        self.assertEqual(expected_response, response)
