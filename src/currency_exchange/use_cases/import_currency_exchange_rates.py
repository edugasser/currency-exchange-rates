import csv
import datetime
from decimal import Decimal

from src.currency_exchange.repository import CurrencyExchangeRepository


class ImportCurrencyExchangeRates(object):
    """
    Using this website to download historical exchange rates:
    > https://excelrates.com.
    """
    def __init__(self, exchange_repository: CurrencyExchangeRepository):
        self.exchange_repository = exchange_repository

    @staticmethod
    def read_file(file_name):
        reader = csv.reader(
            open(file_name, "r"),
            delimiter=";"
        )
        return reader

    @staticmethod
    def parse_row(row):
        valuation_date = datetime.datetime.strptime(row[0], '%d %b %Y').date()
        rate_value = Decimal(row[2])
        return valuation_date, rate_value

    def execute(self, file_name: str):
        source, target, first = None, None, True
        for row in self.read_file(file_name):
            if first:
                source, target = row[1], row[2]
                first = False
                continue

            valuation_date, rate_value = self.parse_row(row)

            self.exchange_repository.save(
                source,
                target,
                rate_value,
                valuation_date
            )
