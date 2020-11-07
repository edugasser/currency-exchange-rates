import datetime

from django.core.management.base import BaseCommand

from src.currency_exchange.use_cases.exchange_updater import UpdateExchange


class UpdateCurrencyExchanges(BaseCommand):
    help = "Update daily currency exchanges"

    def handle(self, *args, **options):
        UpdateExchange().update(datetime.date.today())
