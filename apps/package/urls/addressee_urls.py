
from django.urls import path
from apps.package.views.addressee_views import *

urlpatterns = [
    path('',addressee_view,name='addressee_view'),
    path('addressee_create/',addressee_create,name='addressee_create'),
    path('addressee_table_results/',addressee_table_results,name='addressee_table_results'),
    path('addressee_update/<int:pk>/',addressee_update,name='addressee_update'),
    
]

