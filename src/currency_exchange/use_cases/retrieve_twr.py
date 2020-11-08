from datetime import date, timedelta
from decimal import Decimal

from src.currency_exchange.repository import CurrencyExchangeRepository
from src.currency_exchange.use_cases.retrieve_currency_exchange import \
    RetrieveCurrencyExchange
from src.utils import iter_days


class RetrieveTWR(object):

    def __init__(self, currency_exchange_repo: CurrencyExchangeRepository):
        self.retriever = RetrieveCurrencyExchange(currency_exchange_repo)

    def run(
        self,
        source_currency: str,
        target_currency: str,
        amount: Decimal,
        date_invested: date
    ) -> Decimal:
        twr = 1
        rate = self.retriever.get(source_currency, target_currency, date_invested)  # noqa
        initial_value = rate * amount

        for day in iter_days(date_invested+timedelta(days=1), date.today()):
            rate = self.retriever.get(source_currency, target_currency, day)
            end_value = rate * amount
            hp = ((end_value - initial_value) / initial_value) * 100
            twr *= 1 + hp
            initial_value = end_value

        twr -= 1
        return twr
