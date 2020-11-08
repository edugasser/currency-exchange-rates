from datetime import date
from decimal import Decimal

from src.currency_exchange.exchange_retriever.exchange_provider import \
    ExchangeProvider
from src.currency_exchange.repository import CurrencyExchangeRepository
from src.currency_exchange.use_cases.obtain_active_provider import \
    ObtainActiveProvider
from src.exceptions import ExchangeCurrencyDoesNotExist


class RetrieveCurrencyExchange(object):

    def __init__(self, exchange_repository: CurrencyExchangeRepository):
        self.exchange_repository = exchange_repository
        self.obtain_active_provider = ObtainActiveProvider(exchange_repository)

    @staticmethod
    def get_exchange_rate_data(
        source_currency,
        exchanged_currency,
        valuation_date,
        provider
    ) -> Decimal:
        exchange_response = ExchangeProvider(provider).get(
            source_currency,
            [exchanged_currency],
            valuation_date
        )
        if not exchange_response.success:
            raise ExchangeCurrencyDoesNotExist(
                "The {source_currency} doesn't has exchange for {exchanged_currency}"  # noqa
            )
        return Decimal(exchange_response.rates[0].rate)

    def get(
        self,
        source_currency: str,
        exchanged_currency: str,
        valuation_date: date = None
    ) -> Decimal:
        if not valuation_date:
            valuation_date = date.today()

        try:
            currency_rate = self.exchange_repository.get(
                source_currency,
                exchanged_currency,
                valuation_date
            )
        except ExchangeCurrencyDoesNotExist:
            provider = self.obtain_active_provider.get()
            currency_rate = self.get_exchange_rate_data(
                source_currency,
                exchanged_currency,
                valuation_date,
                provider
            )
        return currency_rate
