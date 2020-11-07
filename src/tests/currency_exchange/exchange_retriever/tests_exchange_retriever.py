import datetime

from django.test import TestCase
from mock import Mock

from src.currency_exchange.exchange_retriever.exchange_providers.mock import \
    MockProvider
from src.currency_exchange.exchange_retriever.exchange_provider import \
    ExchangeProvider


class ExchangeRetrieverTestCase(TestCase):

    def setUp(self):
        self.provider = MockProvider()
        self.retriver = ExchangeProvider(self.provider)
        self.today = datetime.date.today()

    def test_get_exchange_for_today(self):
        # Given
        self.provider.get_latest = Mock()
        # When
        self.retriver.get("EUR", ["COP", "USD"], self.today)
        # Then
        self.provider.get_latest.assert_called_once_with("EUR", ["COP", "USD"])

    def test_get_exchange_for_past_day(self):
        # Given
        self.provider.get_historical = Mock()
        valuation_date = datetime.date(1970, 1, 1)

        # When
        self.retriver.get("EUR", ["COP", "USD"], valuation_date)

        # Then
        self.provider.get_historical.assert_called_once_with(
            "EUR",
            ["COP", "USD"],
            valuation_date
        )


