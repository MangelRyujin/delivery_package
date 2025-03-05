
from django.urls import path
from apps.package.views.customer_order import customer_package_detail
from apps.package.views.package_views import *


urlpatterns = [
    path('',packages_view,name='packages_view'),
    path('packages_results_view/',packages_results_view,name='packages_results_view'),
    path('package_create/',package_create,name='package_create'),
    path('package_detail/<int:pk>/',package_detail,name='package_detail'),
    path('customer_package_detail/<int:pk>/',customer_package_detail,name='customer_package_detail'),
    path('package_delete/<int:pk>/',package_delete,name='package_delete'),
    path('package_get_addressee/',package_get_addressee,name='package_get_addressee'), 
    path('package_get_addressee_update/<int:pk>/',package_get_addressee_update,name='package_get_addressee_update'), 
    path('package_update/<int:pk>/',package_update,name='package_update'),
    path('package_information_update/<int:pk>/',package_information_update,name='package_information_update'),
    path('package_images_update/<int:pk>/',package_images_update,name='package_images_update'),
    path('package_images_delete/<int:pk>/',package_images_delete,name='package_images_delete'),
    path('package_payment_update/<int:pk>/',package_payment_update,name='package_payment_update'),
    path('package_component_table_detail/<int:pk>/',package_component_table_detail,name='package_component_table_detail'),
    path('package_component_table_payment/<int:pk>/',package_component_table_payment,name='package_component_table_payment'),
    path('package_component_table_delivery/<int:pk>/',package_component_table_delivery,name='package_component_table_delivery'),

]

