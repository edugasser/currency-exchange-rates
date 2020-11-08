from src.currency_exchange.exchange_retriever.exchange_factory_provider import \
    ExchangeFactoryProvider
from src.currency_exchange.use_cases.retrieve_currency_exchange_rate import \
    CurrencyExchangeRepository, RetrieveCurrencyExchangeRate
from src.exceptions import ExchangeCurrencyDoesNotExist, ExchangeCurrencyError


class UpdateCurrencyExchangeRate(object):

    def __init__(self, exchange_repository: CurrencyExchangeRepository):
        self.exchange_repository = exchange_repository
        self.provider = ExchangeFactoryProvider(exchange_repository).get()

    @staticmethod
    def iter(currencies):
        for source_currency in currencies:
            for exchanged_currency in currencies:
                if source_currency == exchanged_currency:
                    continue
                yield source_currency, exchanged_currency

    def update(
        self,
        source_currency,
        exchanged_currency,
        valuation_date
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
            rate
        )

    def update_all(self, valuation_date):
        currencies = self.exchange_repository.get_all_currencies()
        for source_currency, exchanged_currency in self.iter(currencies):
            try:
                self.update(source_currency, exchanged_currency, valuation_date)  # noqa
            except (ExchangeCurrencyDoesNotExist, ExchangeCurrencyError) as e:
                # TODO: logging
                pass
