from datetime import date, datetime
from decimal import Decimal

import requests
from django.conf import settings

from app.celery import app
from currency_converter.tasks import updating_exchange_rate
from orders.models import Orders
from currency_converter.models import Currencies

API_KEY: str = settings.API_KEY
SPREADSHEET_ID: str = settings.SPREADSHEET_ID
TODAY = date.today()


def delete_data_sheets(data_list: list):
    """Удаляем данные, которых нет в гугл таблице"""
    data_for_delete = Orders.objects.filter().exclude(id__in=data_list)
    if data_for_delete.exists():
        return data_for_delete.delete()


def update_data_sheets(order: Orders, order_dict: dict):
    """Актуализация данных"""
    if not order.order_cost_usd == order_dict.get('order_cost_usd'):
        order.order_cost_usd = order_dict.get('order_cost_usd')
    if not order.order_cost_rub == order_dict.get('order_cost_rub'):
        order.order_cost_rub = order_dict.get('order_cost_rub')
    if not order.delivery_time == order_dict.get('delivery_time'):
        order.delivery_time = order_dict.get('delivery_time')
        if order.delivery_time.date() > TODAY:
            order.delivery_overdue = False
        else:
            order.delivery_overdue = True
    order.save()


def parser_requests_date():
    """Делаем запрос на google API, указывая ID таблицы и свой API KEY"""
    url: str = (
        'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}?includeGridData=true&key={api_key}'.format(
            spreadsheet_id=SPREADSHEET_ID, api_key=API_KEY
        ))
    main_data = None
    response = requests.get(url)
    data_dict = response.json()
    if data_dict:
        data_1 = data_dict.get('sheets', None)
        if data_1:
            data_2 = data_1[0].get('data', None)
            if data_2:
                main_data = data_2[0].pop('rowData')
    return main_data


def get_actual_course():
    """Получаем актуальный курс"""
    curse = Currencies.objects.filter().only('rub', 'id').order_by('-id').first()
    if curse:
        rubles: Decimal = curse.rub
    else:
        count = 1
        print('Актуального курса в базе данных не найдено!')
        print('Пытаюсь обновить курс валют...')
        print('_' * 50)
        while curse is None and count <= 10:
            print(f'Попытка № {count}')
            updating_exchange_rate()
            curse = Currencies.objects.filter().only('rub').first()
            count += 1
        print('_' * 50)
        print('Курс обновлен.')
        rubles: Decimal = curse.rub
    return rubles


@app.task
def table_parser():
    """Основной парсер гугл таблицы"""

    list_data_ids = []
    values_dict = {
        0: 'self_number',
        1: 'order_cost',
        2: 'delivery_time',
    }

    main_data = parser_requests_date()
    rubles: Decimal = get_actual_course()

    if main_data:
        for el in main_data[1:]:
            order_dict = {}
            values = el.get('values', None)
            if values:
                for ids, value in enumerate(values[1:]):
                    data = value.get('formattedValue', None)
                    if data:
                        key = values_dict.get(ids)
                        if key == 'self_number':
                            order_dict[key] = data
                        elif key == 'order_cost':
                            order_dict['order_cost_usd'] = Decimal(data)
                            price = Decimal(data) * rubles
                            order_dict['order_cost_rub'] = price
                        elif key == 'delivery_time':
                            data_date = datetime.strptime(data, '%d.%m.%Y')
                            order_dict[key] = data_date
                            if data_date.date() < TODAY:
                                order_dict['delivery_overdue'] = True
                    continue
            if order_dict:
                order = Orders.objects.filter(self_number=order_dict.get('self_number')).first()
                if order:
                    # Тут собираем ID заказов, чтобы потом сверить наличие данных в таблице и в БД
                    list_data_ids.append(order.id)
                    # Тут сверяем и обнвляем данные в таблице
                    update_data_sheets(order, order_dict)
                    continue
                Orders.objects.create(**order_dict)
        if list_data_ids:
            delete_data_sheets(list_data_ids)
