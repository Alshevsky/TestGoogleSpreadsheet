from django.contrib import admin

from ..models import Currencies


@admin.register(Currencies)
class CurrenciesAdmin(admin.ModelAdmin):
    pass

