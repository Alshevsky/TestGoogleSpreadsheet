import requests
import xmltodict

from datetime import datetime
from decimal import Decimal

from django.conf import settings

from app.celery import app
from currency_converter.exceptions import ValuteException
from currency_converter.models import Currencies

today = datetime.today().date()
data = requests.get(settings.CBR_RU_URL)
dict_data: dict = xmltodict.parse(data.content)


@app.task
def updating_exchange_rate():
    """Собираем актуальный курс рубля"""
    today_currencies = Currencies.objects.filter(dated=today).exists()
    if today_currencies:
        return print('Курс уже актуальный')
    for key, value in dict_data.items():
        currencies = value.get('Valute', None)
        if currencies:
            for el in currencies:
                if el['Name'] == 'Доллар США':
                    price = el.get('Value', None)
                    if price:
                        price = Decimal(price.replace(',', '.'))
                        Currencies.objects.create(rub=price)
                        break
                    raise ValuteException

