from src.currency_exchange.use_cases.obtain_active_provider import \
    ObtainActiveProvider
from src.currency_exchange.use_cases.retrieve_currency_exchange import \
    CurrencyExchangeRepository, RetrieveCurrencyExchange


class UpdateExchange(object):

    def __init__(self, exchange_repository: CurrencyExchangeRepository):
        self.exchange_repository = exchange_repository
        self.provider = ObtainActiveProvider(exchange_repository).get()

    def update_all(self, valuation_date):
        currencies = self.exchange_repository.get_all_currencies()

        for source_currency in currencies:
            for exchanged_currency in currencies:
                if source_currency == exchanged_currency:
                    continue

                rate = RetrieveCurrencyExchange.get_exchange_rate_data(
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
