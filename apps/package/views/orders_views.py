from apps.account.models import User
from apps.package.filters import OrderFilter
from apps.package.forms.package_forms import  CreateOrderForm, PackageForm, UpdateOrderForm
from apps.package.models import  Order, Package
from django.shortcuts import render,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
import logging
from apps.account.decorators import group_required
from utils.paginator import _create_paginator
from utils.send_email import order_in_proccess_send_customer_email, send_email_to_customer
logger = logging.getLogger(__name__)
from django.db.models import Q
from django.utils.translation import gettext as _
from datetime import date
  
# orders index 
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def orders_view(request):
    orders = Order.objects.filter(state__in=['1','2']).order_by('-id')
    context = {
        'admin':User.objects.all(),
        'orders':orders,
        'form': CreateOrderForm(),
        'packages': Package.objects.filter(state='2').exclude(orders__isnull=False).order_by('pk')
        }
    response= render(request,'orders_proccess/order.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# orders search result
@staff_member_required(login_url='/')
def orders_results_view(request):
    return  render(request,'orders_proccess/order_result.html',context=_show_orders(request))
       
# orders search funtion
@staff_member_required(login_url='/')
def _show_orders(request):
    return _create_paginator(request,OrderFilter(request.GET, queryset=Order.objects.filter(state__in=['1','2']).order_by('-pk')))
    
   


# order detail forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def order_detail(request,pk):
    order = Order.objects.filter(pk=pk,state__in=['1','2']).first()
    context={'order':order}
    return render(request,'orders_proccess/actions/orderDetail/orderDetail.html',context) 


# order detail forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def order_component_table_detail(request,pk):
    order = Order.objects.filter(pk=pk,state__in=['1','2']).first()
    context={'order':order}
    return render(request,'orders_proccess/order_table_component.html',context) 

# order detail forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def order_component_table_update_to_finished(request,pk):
    order = Order.objects.filter(pk=pk,state__in=['1','2']).first()
    context={'order':order}
    if order:
        if order.state=='1':
            order.state='2'
            order_in_proccess_send_customer_email(order)    
        else:
            order.state='3'
            order.delivery_date = date.today()
        order.save()
        if order.state == '3':
            order = []
        context['order']=order
    return render(request,'orders_proccess/order_table_component.html',context) 


# Delete order result table
@group_required('administrador')
@staff_member_required(login_url='/')
def order_delete(request,pk):
    order = Order.objects.filter(pk=pk).first()
    context={
        'order':order,
        
    }
    if request.method == "POST":
        if order:
            order.delete()
            context['order']=[]
            return  render(request,'orders_proccess/order_table_component.html',context)
    return  render(request,'orders_proccess/actions/orderDelete/orderDeleteVerify.html',context)


# Create order result table
@group_required('administrador')
@staff_member_required(login_url='/')
def order_create(request):
    form = CreateOrderForm()
    context={
        'form':form,
    }
    if request.method == "POST":
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            form.save()
            context['message']='Envío creado correctamente'
    context['packages']=Package.objects.filter(state='2',type='1').exclude(orders__isnull=False).order_by('pk')
    return  render(request,'orders_proccess/actions/orderCreate/orderCreateForm.html',context)

# order get package

@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def order_get_package(request):
    type =request.GET.get('type',None) 
    packages = Package.objects.filter(state='2',type=type).exclude(orders__isnull=False).order_by('-pk') if type  else []
    context={'packages':packages}
    return render(request,'orders_proccess/actions/orderCreate/select_package.html',context) 

# order update forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def order_update(request,pk):
    order = Order.objects.filter(pk=pk).first()
    context={
        'form':UpdateOrderForm(instance=order),
        'order':order,
        'packages': Package.objects.filter(state='2',type=order.type).exclude(orders__isnull=False).order_by('pk'),
        'select_packages': Package.objects.filter(state='2').filter(orders=order).order_by('pk')
        }
    if request.method == 'POST':
        form =   UpdateOrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            if order.state == '3':
                order.delivery_date = date.today()
                order.save()
            order_in_proccess_send_customer_email(order)      
            context['form']=form
            context['message']="Editado correctamente"
        
    return render(request,'orders_proccess/actions/orderUpdate/orderUpdateForm.html',context) 