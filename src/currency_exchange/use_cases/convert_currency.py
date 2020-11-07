from decimal import Decimal

from src.currency_exchange.models import Currency
from src.currency_exchange.repository import currency_exchange_repository
from src.currency_exchange.use_cases.retrieve_currency_exchange import \
    RetrieveCurrencyExchange
from src.exceptions import CurrencyDoesNotExist
from collections import namedtuple

converted_currency = namedtuple(
    "ConvertedCurrency",
    "origin target amount converted_amount"
)


class ConvertCurrency(object):

    def __init__(self):
        self.valid_currencies = Currency.objects.all().values_list(
            'code',
            flat=True
        )
        self.retrieve_currency_exchange = RetrieveCurrencyExchange(
            currency_exchange_repository
        )

    def validate_currencies(self, origin, target):
        if origin not in self.valid_currencies:
            raise CurrencyDoesNotExist(f"The currency {origin} doesn't exist")

        if target not in self.valid_currencies:
            raise CurrencyDoesNotExist(f"The currency {target} doesn't exist")

    def convert(self, origin_currency: str, amount: Decimal,  target_currency: str):  # noqa
        self.validate_currencies(origin_currency, target_currency)
        rate = self.retrieve_currency_exchange.get(
            origin_currency,
            target_currency
        )
        converted_amount = amount * rate if amount else 0.
        return converted_currency(
            origin_currency,
            target_currency,
            amount,
            converted_amount
        )
