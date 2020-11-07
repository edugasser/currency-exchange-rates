import datetime

from django.test import TestCase
from mock import Mock

from src.currency_exchange.constants import TypeProvider
from src.currency_exchange.exchange_retriever.exchange_providers.mock import \
    MockProvider
from src.currency_exchange.exchange_retriever.exchange_response import \
    ExchangeResponse, CurrencyRate
from src.currency_exchange.use_cases.retrieve_exchange import RetrieveExchange, \
    CurrencyExchangeRepository
from src.exceptions import ExchangeCurrencyDoesNotExist


class MockRepository(CurrencyExchangeRepository):

    def get_active_provider(self):
        return TypeProvider.MOCK

    def get(self, source_currency, exchanged_currency, valuation_date):
        return 10.


class RetrieveExchangeTestCase(TestCase):

    def setUp(self):
        self.repository = MockRepository()
        self.retriever = RetrieveExchange(self.repository)

    def test_get_exchange_from_repository(self):
        # Given
        self.repository.get = Mock(return_value=99)
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
        self.repository.get = Mock(side_effect=ExchangeCurrencyDoesNotExist("test"))
        self.retriever.obtain_active_provider = Mock(
            return_value=MockProvider()
        )
        valuation_date = datetime.date.today()

        # When
        rate = self.retriever.get("EUR", "USD", valuation_date)

        # Then
        self.assertEqual(True, isinstance(rate, float))
        self.retriever.obtain_active_provider.assert_called_once_with()

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
