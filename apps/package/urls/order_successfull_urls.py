
from django.urls import path
from apps.package.views.orders_successfull_views import *

urlpatterns = [
    path('',orders_successfull_views,name='orders_successfull_views'),
    path('orders_successfull_results_view/',orders_successfull_results_view,name='orders_successfull_results_view'),
    path('orders_successfull_detail/<int:pk>/',orders_successfull_detail,name='orders_successfull_detail'),
]

