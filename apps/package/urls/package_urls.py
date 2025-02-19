
from django.urls import path
from apps.package.views.package_views import *

urlpatterns = [
    path('',packages_view,name='packages_view'),
    path('packages_results_view/',packages_results_view,name='packages_results_view'),
]

