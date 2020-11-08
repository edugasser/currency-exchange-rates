from collections import namedtuple
from decimal import Decimal

from src.currency_exchange.repository import currency_exchange_repository, \
    CurrencyExchangeRepository
from src.currency_exchange.use_cases.retrieve_currency_exchange_rate import \
    RetrieveCurrencyExchangeRate
from src.exceptions import CurrencyDoesNotExist
from src.utils import round_decimal

converted_currency = namedtuple(
    "ConvertedCurrency",
    "origin target amount converted_amount"
)


class ConvertCurrency(object):

    def __init__(self, currency_repository: CurrencyExchangeRepository):
        self.currency_repository = currency_repository
        self.retrieve_currency_exchange = RetrieveCurrencyExchangeRate(
            currency_exchange_repository
        )

    def validate_currencies(self, origin, target):
        valid_currencies = self.currency_repository.get_all_currencies()
        if origin not in valid_currencies:
            raise CurrencyDoesNotExist(f"The currency {origin} doesn't exist")

        if target not in valid_currencies:
            raise CurrencyDoesNotExist(f"The currency {target} doesn't exist")

    def convert(self, origin_currency: str, amount: Decimal,  target_currency: str):  # noqa
        self.validate_currencies(origin_currency, target_currency)
        rate = self.retrieve_currency_exchange.get(
            origin_currency,
            target_currency
        )

        converted_amount = round_decimal(amount * rate if amount else 0.)
        return converted_currency(
            origin_currency,
            target_currency,
            amount,
            converted_amount
        )
