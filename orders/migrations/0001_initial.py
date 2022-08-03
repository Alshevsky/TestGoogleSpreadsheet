# Generated by Django 4.1 on 2022-08-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('self_number', models.PositiveIntegerField(verbose_name='Номер заказа')),
                ('order_cost_usd', models.DecimalField(decimal_places=2, default=0, max_digits=1000, verbose_name='Стоимость заказа (USD)')),
                ('order_cost_rub', models.DecimalField(decimal_places=2, default=0, max_digits=1000, verbose_name='Стоимость заказа (RUB)')),
                ('delivery_time', models.DateField(blank=True, null=True, verbose_name='Срок поставки заказа')),
                ('delivery_overdue', models.BooleanField(blank=True, default=False, verbose_name='Заказ просрочен')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
