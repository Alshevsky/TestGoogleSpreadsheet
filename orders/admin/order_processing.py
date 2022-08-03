from django.contrib import admin

from ..models import Orders


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['self_number', 'order_cost_usd', 'order_cost_rub', 'delivery_time', 'delivery_overdue']
    list_filter = ['delivery_time', 'delivery_overdue']
