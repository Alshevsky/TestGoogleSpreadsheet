from decimal import Decimal
from datetime import date

from django.db import models
from django.db.models import Manager


class Currencies(models.Model):
    usd: Decimal = models.DecimalField('USD', max_digits=100, decimal_places=4, default=1.0, blank=True)
    rub: Decimal = models.DecimalField('RUB', max_digits=100, decimal_places=4)
    dated: date = models.DateField('Дата курса', auto_now_add=True)

    objects = Manager()

    class Meta:
        verbose_name = 'Курс валюты'
        verbose_name_plural = 'Курс валют'

    def __str__(self):
        return f'{self.usd} USD - {self.rub} RUB, DATE: {self.dated}'
