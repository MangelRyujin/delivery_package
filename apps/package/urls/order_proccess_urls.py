
from django.urls import path
from apps.package.views.orders_views import *

urlpatterns = [
    path('',orders_view,name='orders_view'),
    path('orders_results_view/',orders_results_view,name='orders_results_view'),
    path('order_create/',order_create,name='order_create'),
    path('order_component_table_detail/<int:pk>/',order_component_table_detail,name='order_component_table_detail'),
    path('order_delete/<int:pk>/',order_delete,name='order_delete'),
   
    
    
]

