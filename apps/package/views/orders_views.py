from apps.account.models import User
from apps.package.forms.package_forms import  CreateOrderForm, PackageForm
from apps.package.models import  Order, Package
from django.shortcuts import render,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
import logging
from apps.account.decorators import group_required
logger = logging.getLogger(__name__)
from django.db.models import Q
from django.utils.translation import gettext as _
  
# orders index 
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def orders_view(request):
    orders = Order.objects.filter(state__in=['1','2']).order_by('-id')
    context = {
        'admin':User.objects.all(),
        'orders':orders,
        'form': CreateOrderForm(),
        'packages': Package.objects.filter(state='2').order_by('pk')
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
    keyword = request.session.get('keyword', '')
    
    if request.method == 'POST':
        keyword = request.POST.get("keyword",'')
        request.session['keyword'] = keyword

    orders = Order.objects.filter(
        Q(pk__icontains=keyword)  ,state__in=['1','2']
        ).distinct().order_by('-id')
    context={
        'orders':orders,
        
    }
    return context


# order detail forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def order_component_table_detail(request,pk):
    order = Order.objects.filter(pk=pk,state='1').first()
    context={'order':order}
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
        'packages': Package.objects.filter(state='2').order_by('pk')
    }
    if request.method == "POST":
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            form.save()
            context['message']='Envío creado correctamente'
            
        else:
            print(form.errors)
    return  render(request,'orders_proccess/actions/orderCreate/orderCreateForm.html',context)