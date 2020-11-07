from app.currency_exchange.repository import currency_exchange_repository
from app.currency_exchange.use_cases.retrieve_exchange import \
    get_exchange_rate_data


class UpdateExchange(object):

    def __init__(self):
        self.currency_exchange_repo = currency_exchange_repository.get_active_provider()  # noqa

    def update(self, valuation_date):
        currencies = self.currency_exchange_repo.get_all_currencies()

        for source_currency in currencies:
            for exchanged_currency in currencies:

                if source_currency == exchanged_currency:
                    continue

                rate = get_exchange_rate_data(
                    source_currency,
                    exchanged_currency,
                    valuation_date,
                    self.currency_exchange_repo.get_active_provider()
                )

                self.currency_exchange_repo.save(
                    source_currency,
                    exchanged_currency,
                    rate
                )
