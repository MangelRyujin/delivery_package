from django.urls import path,include
from apps.general.views.general_views import dashboard_view
from apps.account.views.admin_views import change_information

urlpatterns = [
    path('',dashboard_view,name='dashboard_view'),
    path('admins/',include('apps.account.urls.admin_urls')),
    path('customers/',include('apps.package.urls.customer_urls')),
    path('addressees/',include('apps.package.urls.addressee_urls')),
    path('packages/',include('apps.package.urls.package_urls')),
    path('order_in_proccess/',include('apps.package.urls.order_proccess_urls')),
    path('perfil/', change_information, name='change_information'),
    

]

