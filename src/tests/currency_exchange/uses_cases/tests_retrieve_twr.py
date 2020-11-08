import datetime
from decimal import Decimal

from django.test import TestCase

from src.currency_exchange.models import Currency, CurrencyExchangeRate
from src.currency_exchange.repository import currency_exchange_repository
from src.currency_exchange.use_cases.retrieve_twr import RetrieveTWR


class RetrieveTwrTestCase(TestCase):

    def setUp(self):
        self.retrieve_twr = RetrieveTWR(currency_exchange_repository)
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(days=1)

        euro = Currency.objects.create(code="EUR", name="Euro", symbol="€")
        usd = Currency.objects.create(code="USD", name="Dollar", symbol="$")

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

    # def test_retrieve_twr(self):
    #     twr = self.retrieve_twr.run("EUR", "USD", Decimal(50), self.yesterday)
    #     self.assertEqual(twr, Decimal(225))
