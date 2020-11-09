from datetime import date

from django.db.transaction import atomic

from src.currency_exchange.exchange_retriever.exchange_factory_provider import ExchangeFactoryProvider  # noqa
from src.currency_exchange.use_cases.retrieve_currency_exchange_rate import \
    CurrencyExchangeRepository, RetrieveCurrencyExchangeRate
from src.exceptions import ExchangeCurrencyDoesNotExist, ExchangeCurrencyError
from src.logger import logger, _


class UpdateCurrencyExchangeRate(object):

    def __init__(self, exchange_repository: CurrencyExchangeRepository):
        self.exchange_repository = exchange_repository
        self.provider = ExchangeFactoryProvider(exchange_repository).get()

    def iter_currencies(self):
        currencies = self.exchange_repository.get_all_currencies()
        for source_currency in currencies:
            for exchanged_currency in currencies:
                if source_currency == exchanged_currency:
                    continue
                yield source_currency, exchanged_currency

    def update(
        self,
        source_currency: str,
        exchanged_currency: str,
        valuation_date: date
    ):
        rate = RetrieveCurrencyExchangeRate.get_exchange_rate_data(
            source_currency,
            exchanged_currency,
            valuation_date,
            self.provider
        )

        self.exchange_repository.save(
            source_currency,
            exchanged_currency,
            rate,
            valuation_date
        )

    @atomic
    def update_all(self, valuation_date: date):
        for source_currency, exchanged_currency in self.iter_currencies():
            try:
                self.update(source_currency, exchanged_currency, valuation_date)  # noqa
            except (ExchangeCurrencyDoesNotExist, ExchangeCurrencyError) as e:
                logger.error(
                    _(
                        "Update all",
                        valuation_date=valuation_date,
                        error=str(e)
                      )
                )
