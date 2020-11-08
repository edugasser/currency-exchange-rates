from django.contrib import admin
from . import models


@admin.register(models.Provider)
class ProviderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass
