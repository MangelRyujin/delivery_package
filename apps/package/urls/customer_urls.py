
from django.urls import path
from apps.package.views.customer_views import *

urlpatterns = [
    path('',customer_view,name='customer_view'),
    path('customer_create/',customer_create,name='customer_create'),
    path('customer_table_results/',customer_table_results,name='customer_table_results'),
    path('customer_update/<int:pk>/',customer_update,name='customer_update'),
    
]

