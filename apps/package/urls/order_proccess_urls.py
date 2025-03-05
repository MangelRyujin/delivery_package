
from django.urls import path
from apps.package.views.orders_views import *

urlpatterns = [
    path('',orders_view,name='orders_view'),
    path('orders_results_view/',orders_results_view,name='orders_results_view'),
    path('order_create/',order_create,name='order_create'),
    path('order_detail/<int:pk>/',order_detail,name='order_detail'),
    path('order_component_table_detail/<int:pk>/',order_component_table_detail,name='order_component_table_detail'),
    path('order_update/<int:pk>/',order_update,name='order_update'),
    path('order_delete/<int:pk>/',order_delete,name='order_delete'),
    path('order_component_table_update_to_finished/<int:pk>/',order_component_table_update_to_finished,name='order_component_table_update_to_finished'),
    path('order_get_package/',order_get_package,name='order_get_package'),
    
    
]

