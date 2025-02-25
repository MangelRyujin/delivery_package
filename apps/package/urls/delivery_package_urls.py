
from django.urls import path
from apps.package.views.customer_order import customer_package_detail
from apps.package.views.delivery_package_view import *


urlpatterns = [
    path('',delivery_packages_view,name='delivery_packages_view'),
    path('delivery_packages_results_view/',delivery_packages_results_view,name='delivery_packages_results_view'),
    path('delivery_package_detail/<int:pk>/',delivery_package_detail,name='delivery_package_detail'),
    path('delivery_package_component_table_detail/<int:pk>/',delivery_package_component_table_detail,name='delivery_package_component_table_detail'),
    path('delivery_package_checked/<int:pk>/',delivery_package_checked,name='delivery_package_checked'),
]

