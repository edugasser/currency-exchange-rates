import datetime

from django.test import TestCase
from mock import patch, Mock, call

from src.currency_exchange.use_cases.update_currency_exchange_rate import \
    UpdateCurrencyExchangeRate
from src.tests.mock_repository import MockRepository


class UpdateExchangeTestCase(TestCase):

    def setUp(self):
        self.repository = MockRepository()
        self.updater = UpdateCurrencyExchangeRate(self.repository)

    @patch('src.currency_exchange.use_cases.retrieve_currency_exchange.RetrieveCurrencyExchange.get_exchange_rate_data')  # noqa
    def test_update_all_currencies(self, get_exchange_rate_data):
        # Given
        get_exchange_rate_data.return_value = 10
        valuation_date = datetime.date.today()
        self.repository.save = Mock()
        today = datetime.date.today()

        # When
        self.updater.update_all(valuation_date)

        # Then
        get_exchange_rate_data.assert_has_calls([
            call('EUR', 'USD', today, self.updater.provider),
            call('USD', 'EUR', today, self.updater.provider)
        ])

        self.repository.save.assert_has_calls(
            [
                call('EUR', 'USD', 10),
                call('USD', 'EUR', 10)
            ]
        )
