from django.db import models


class Provider(models.Model):
    class TypeProvider(models.TextChoices):
        FIXER_IO = 'FIXER', 'Fixer Io'
        MOCK = 'MOCK', 'Mock'

    provider = models.CharField(
        max_length=5,
        choices=TypeProvider.choices,
        default=TypeProvider.MOCK
    )
    order = models.PositiveSmallIntegerField()
    config = models.JSONField(blank=True)


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)


class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(
        Currency,
        related_name='exchanges',
        on_delete=models.CASCADE
    )
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(
        db_index=True,
        decimal_places=6,
        max_digits=18
    )


