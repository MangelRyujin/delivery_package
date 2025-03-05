from django.urls import path,include
from apps.general.views.general_views import dashboard_view
from apps.account.views.admin_views import change_information
from apps.package.views.customer_order import customer_orders_view
from apps.package.views.send_email import validate_customer_orders_view

urlpatterns = [
    path('',dashboard_view,name='dashboard_view'),
    path('admins/',include('apps.account.urls.admin_urls')),
    path('customers/',include('apps.package.urls.customer_urls')),
    path('addressees/',include('apps.package.urls.addressee_urls')),
    path('packages/',include('apps.package.urls.package_urls')),
    path('order_in_proccess/',include('apps.package.urls.order_proccess_urls')),
    path('orders_successfull/',include('apps.package.urls.order_successfull_urls')),
    path('perfil/', change_information, name='change_information'),
    path('validate_customer/', validate_customer_orders_view, name='validate_customer_orders_view'),
    path('customer_orders/', customer_orders_view, name='customer_orders_view'),
    path('delivery_packages/',include('apps.package.urls.delivery_package_urls')),

]

