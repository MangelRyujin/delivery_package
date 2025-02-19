from django.shortcuts import render,get_object_or_404
from apps.account.decorators import group_required
import logging
from apps.package.filters import CustomerFilter
from apps.package.models import Customer
from apps.package.forms.customer_forms import CustomerForm
from utils.paginator import _create_paginator
logger = logging.getLogger(__name__)
from django.contrib.admin.views.decorators import staff_member_required


# local view (index)
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def customer_view(request):
    response= render(request,'customer_templates/customer.html',{'form':CustomerForm()})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Charge result table
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def customer_table_results(request):
    return  render(request,'customer_templates/customer_table_results.html',context=_show_customer(request))


# customer create form
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def customer_create(request):
    context={
        'form':CustomerForm()
    }
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()  
            context['message']='customere creado correctamente'
        context['form']=form
    return render(request,'customer_templates/actions/customerCreate/customerCreateForm.html',context) 

# customer update forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def customer_update(request,pk):
    customer = get_object_or_404(Customer,pk=pk)
    form = CustomerForm(instance=customer)
    context={
    }
    if request.method == "POST":
        form = CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            context['message']='Editado correctamente'
        else:
            message="Corrige los errores"
            context['error']=message
    context['customer']=customer
    context['form']=form
    return render(request,'customer_templates/actions/customerUpdate/customerUpdateCheckForm.html',context) 

# Show customer table
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def _show_customer(request):
    return _create_paginator(request,CustomerFilter(request.GET, queryset=Customer.objects.all().order_by('email')))