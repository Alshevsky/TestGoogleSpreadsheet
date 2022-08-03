from django.contrib import admin
from django.urls import path

from orders.views.views import data_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', data_info)
]
