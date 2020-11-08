from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .constants import TypeProvider


class Provider(models.Model):
    provider = models.CharField(
        max_length=5,
        choices=TypeProvider.choices,
        default=TypeProvider.MOCK
    )
    default = models.BooleanField()
    #config = JSONField(null=True)

    def __str__(self):
        return f"{self.provider}: {self.default}"


class Currency(models.Model):
    # TODO: Define a choices with all currencies
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.code}: {self.name} (self.symbol)"


class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(
        Currency,
        related_name='exchanges',
        on_delete=models.CASCADE
    )
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(
        decimal_places=6,
        max_digits=18
    )

    def __str__(self):
        return f"{self.source_currency}: {self.exchanged_currency} | {self.valuation_date}"  # noqa

    class Meta:
        # NOTE: Because the system saves daily exchange.
        unique_together = (
            'source_currency',
            'exchanged_currency',
            "valuation_date"
        )


@receiver(post_save, sender=Provider)
def post_save_provider(sender, instance, created=None, **kwargs):
    if instance.default:
        Provider.objects.exclude(id=instance.id).update(default=False)
    else:
        if Provider.objects.filter(default=True).count() != 1:
            raise ValidationError("A default Provider is required")


@receiver(pre_delete, sender=Provider)
def pre_delete_provider(sender, created=None, instance=None, **kwargs):
    if not Provider.objects.filter(default=True).exclude(id=instance.id):
        raise ValidationError("A default Provider is required")
