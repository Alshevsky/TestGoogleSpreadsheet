from django.shortcuts import render

from currency_converter.models import Currencies
from orders.models import Orders


def data_info(request):
    context = {}
    today_currencies = Currencies.objects.filter().order_by('-id').first()
    orders = Orders.objects.all()
    if today_currencies:
        context['currencies'] = today_currencies
    if orders.exists():
        context['orders'] = orders
    return render(request, 'base.html', context)
