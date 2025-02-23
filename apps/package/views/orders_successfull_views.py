from apps.account.models import User
from apps.package.filters import OrderFilter
from apps.package.forms.package_forms import  CreateOrderForm, PackageForm, UpdateOrderForm
from apps.package.models import  Order, Package
from django.shortcuts import render,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
import logging
from apps.account.decorators import group_required
from utils.paginator import _create_paginator
logger = logging.getLogger(__name__)
from django.db.models import Q
from django.utils.translation import gettext as _
  
# orders index 
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def orders_successfull_views(request):
    orders = Order.objects.filter(state='4').order_by('-id')
    context = {
        'orders':orders,
        }
    response= render(request,'orders_successfull/order.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# orders search result
@staff_member_required(login_url='/')
def orders_successfull_results_view(request):
    return  render(request,'orders_successfull/order_result.html',context=_show_orders_successfull(request))
       
# orders search funtion
@staff_member_required(login_url='/')
def _show_orders_successfull(request):
    return _create_paginator(request,OrderFilter(request.GET, queryset=Order.objects.filter(state='4').order_by('-pk')))
    
   


# order detail forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def orders_successfull_detail(request,pk):
    order = Order.objects.filter(pk=pk,state='4').first()
    context={'order':order}
    return render(request,'orders_successfull/actions/orderDetail/orderDetail.html',context) 

