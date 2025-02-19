from django.shortcuts import render,get_object_or_404
from apps.account.decorators import group_required
import logging
from apps.package.filters import AddresseeFilter
from apps.package.models import Addressee, Customer
from apps.package.forms.addressee_forms import AddresseeForm
from utils.paginator import _create_paginator
logger = logging.getLogger(__name__)
from django.contrib.admin.views.decorators import staff_member_required


# local view (index)
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def addressee_view(request):
    context={
        'form':AddresseeForm(),
        'customers': Customer.objects.all()
    }
    response= render(request,'addressee_templates/addressee.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Charge result table
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def addressee_table_results(request):
    return  render(request,'addressee_templates/addressee_table_results.html',context=_show_addressee(request))


# addressee create form
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def addressee_create(request):
    context={
        'form':AddresseeForm(),
        'customers': Customer.objects.all()
    }
    if request.method == "POST":
        form = AddresseeForm(request.POST)
        if form.is_valid():
            form.save()  
            context['message']='addresseee creado correctamente'
        context['form']=form
    return render(request,'addressee_templates/actions/addresseeCreate/addresseeCreateForm.html',context) 

# addressee update forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def addressee_update(request,pk):
    addressee = get_object_or_404(Addressee,pk=pk)
    context={
        'form' : AddresseeForm(instance=addressee),
        'customers': Customer.objects.all()
    }
    if request.method == "POST":
        form = AddresseeForm(request.POST,instance=addressee)
        if form.is_valid():
            form.save()
            context['message']='Editado correctamente'
            context['form']=form
        else:
            message="Corrige los errores"
            context['error']=message
    context['addressee']=addressee
    
    return render(request,'addressee_templates/actions/addresseeUpdate/addresseeUpdateCheckForm.html',context) 

# Show addressee table
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def _show_addressee(request):
    return _create_paginator(request,AddresseeFilter(request.GET, queryset=Addressee.objects.all().order_by('full_name')))