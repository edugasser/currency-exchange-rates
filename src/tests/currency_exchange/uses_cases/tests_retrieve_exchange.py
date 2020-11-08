import datetime
from decimal import Decimal

from django.test import TestCase
from mock import Mock

from src.currency_exchange.exchange_retriever.exchange_providers.mock import \
    MockProvider
from src.currency_exchange.exchange_retriever.exchange_response import \
    ExchangeResponse, CurrencyRate
from src.currency_exchange.use_cases.retrieve_currency_exchange import \
    RetrieveCurrencyExchange
from src.exceptions import ExchangeCurrencyDoesNotExist
from src.tests.mock_repository import MockRepository


class RetrieveExchangeTestCase(TestCase):

    def setUp(self):
        self.repository = MockRepository()
        self.retriever = RetrieveCurrencyExchange(self.repository)

    def test_get_exchange_from_repository(self):
        # Given
        self.repository.get = Mock(return_value=Decimal(99))
        valuation_date = datetime.date.today()

        # When
        currency_rate = self.retriever.get("EUR", "USD", valuation_date)

        # Then
        self.assertEqual(currency_rate, 99)
        self.repository.get.assert_called_once_with(
            "EUR",
            "USD",
            valuation_date
        )

    def test_get_exchange_from_provider(self):
        # Given
        self.repository.get = Mock(side_effect=ExchangeCurrencyDoesNotExist("test"))  # noqa
        self.retriever.obtain_active_provider = Mock()
        self.retriever.obtain_active_provider.get.return_value = MockProvider()

        valuation_date = datetime.date.today()

        # When
        rate = self.retriever.get("EUR", "USD", valuation_date)

        # Then
        self.assertEqual(True, isinstance(rate, Decimal))
        self.retriever.obtain_active_provider.get.assert_called_once_with()

    def test_get_exchange_rate_data_with_unsuccesful_response(self):
        # Given
        provider = MockProvider()
        mock_response = ExchangeResponse(
            False,
            datetime.date.today(),
            "EUR",
            []
        )

        provider.get_latest = Mock(return_value=mock_response)

        # When
        with self.assertRaises(ExchangeCurrencyDoesNotExist):
            self.retriever.get_exchange_rate_data(
                "EUR",
                "USD",
                datetime.date.today(),
                provider
            )

    def test_get_exchange_rate_data_succesful_response(self):
        # Given
        provider = MockProvider()
        mock_response = ExchangeResponse(
            True,
            datetime.date.today(),
            "EUR",
            [CurrencyRate(currency='USD', rate=1.18)]
        )

        provider.get_latest = Mock(return_value=mock_response)

        # When
        result = self.retriever.get_exchange_rate_data(
            "EUR",
            "USD",
            datetime.date.today(),
            provider
        )

        # Then
        self.assertEqual(result, 1.18)
