from decimal import Decimal
from datetime import date

from django.db import models
from django.db.models import Manager


class Orders(models.Model):
    self_number: int = models.PositiveIntegerField('Номер заказа')
    order_cost_usd: Decimal = models.DecimalField('Стоимость заказа (USD)', max_digits=1000,
                                                  decimal_places=2,
                                                  default=0)
    order_cost_rub: Decimal = models.DecimalField('Стоимость заказа (RUB)', max_digits=1000,
                                                  decimal_places=2,
                                                  default=0)
    delivery_time: date = models.DateField('Срок поставки заказа', blank=True, null=True)
    delivery_overdue: bool = models.BooleanField('Заказ просрочен', blank=True, default=False)

    objects = Manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ № {self.self_number}'
