from django.db import models


class CurrencyExchangeRateManager(models.Manager):

    def in_dates(self, from_date, to_date):
        return self.filter(
            valuation_date__gte=from_date,
            valuation_date__lte=to_date
        )
