import datetime

from django.core.management.base import BaseCommand

from src.currency_exchange.repository import currency_exchange_repository
from src.currency_exchange.use_cases.update_currency_exchange_rate import \
    UpdateCurrencyExchangeRate


class Command(BaseCommand):
    help = "Update daily currency exchanges"

    def handle(self, *args, **options):
        UpdateCurrencyExchangeRate(
            currency_exchange_repository
        ).update_all(datetime.date.today())
