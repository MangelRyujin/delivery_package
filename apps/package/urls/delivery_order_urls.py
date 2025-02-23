from django.urls import path
from apps.package.views.reports_users_views import *

urlpatterns = [
    path('',report_delivery_order_view,name='report_delivery_order_view'),
    path('delivery_order_table_results/',delivery_order_table_results,name='delivery_order_table_results'),
]

