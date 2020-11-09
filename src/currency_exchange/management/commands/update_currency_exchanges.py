import datetime

from django.core.management.base import BaseCommand

from src.currency_exchange.use_cases.update_currency_exchange_rate import \
    UpdateCurrencyExchangeRate


class UpdateCurrencyExchanges(BaseCommand):
    help = "Update daily currency exchanges"

    def handle(self, *args, **options):
        UpdateCurrencyExchangeRate().update(datetime.date.today())
