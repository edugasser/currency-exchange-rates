from datetime import date
from decimal import Decimal

from src.currency_exchange.exchange_retriever.exchange_factory_provider import ExchangeFactoryProvider  # noqa
from src.currency_exchange.exchange_retriever.exchange_provider import \
    ExchangeProvider, ExchangeProviderInterface
from src.currency_exchange.repository import CurrencyExchangeRepository
from src.exceptions import ExchangeCurrencyDoesNotExist
from src.logger import logger, _
from src.utils import round_decimal


class RetrieveCurrencyExchangeRate(object):

    def __init__(self, exchange_repository: CurrencyExchangeRepository):
        self.exchange_repository = exchange_repository
        self.factory_provider = ExchangeFactoryProvider(exchange_repository)

    @staticmethod
    def get_exchange_rate_data(
        source_currency: str,
        exchanged_currency: str,
        valuation_date: date,
        provider: ExchangeProviderInterface
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
            msg = "Retrieve exchange from repository:"
        except ExchangeCurrencyDoesNotExist:
            # NOTE: maybe we can save in db the rate for future readings.
            provider = self.factory_provider.get()
            currency_rate = self.get_exchange_rate_data(
                source_currency,
                exchanged_currency,
                valuation_date,
                provider
            )
            msg = "Retrieve exchange from provider:",

        logger.info(_(msg, valuation_date=valuation_date, response=currency_rate))  # noqa
        return round_decimal(currency_rate)
