from apps.package.forms.package_forms import CreateImagePackageForm, PackageForm, UpdatePackageForm
from apps.package.models import ImagePackage, Package,Customer,Addressee
from django.shortcuts import render,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
import logging
from django.forms import modelformset_factory
from apps.account.decorators import group_required
logger = logging.getLogger(__name__)
from django.db.models import Q
from django.utils.translation import gettext as _
from django.db import transaction, IntegrityError
  
# packages index 
@group_required('administrador','repartidor')
@staff_member_required(login_url='/')
def delivery_packages_view(request):
    packages = Package.objects.filter(is_delivery=False,orders__isnull=False,orders__state__in=['2','3'],state='2').order_by('-id')
    context = {
        'packages':packages,
        
        
        }
    response= render(request,'delivery_packages/package.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# packages search result
@staff_member_required(login_url='/')
def delivery_packages_results_view(request):
    return  render(request,'delivery_packages/package_result.html',context=_show_delivery_packages(request))
       
# packages search funtion
@staff_member_required(login_url='/')
def _show_delivery_packages(request):
    keyword = request.session.get('keyword', '')
    
    if request.method == 'POST':
        keyword = request.POST.get("keyword",'')
        request.session['keyword'] = keyword

    packages = Package.objects.filter(
        Q(orders__pk__icontains=keyword) | Q(pk__icontains=keyword) |Q(addressee__full_name__icontains=keyword) 
        | Q(addressee__province__icontains=keyword)|Q(addressee__municipe__icontains=keyword) 
        | Q(addressee__address__icontains=keyword)| Q(addressee__phone_number__icontains=keyword) ,is_delivery=False
        ,orders__isnull=False,orders__state__in=['2','3'],state='2'
        ).distinct().order_by('-id')
    context={
        'packages':packages,
        
    }
    return context


# package detail forms
@group_required('administrador','repartidor')
@staff_member_required(login_url='/')
def delivery_package_component_table_detail(request,pk):
    package = Package.objects.filter(pk=pk,is_delivery=False,state='2').first()
    context={'package':package}
    return render(request,'delivery_packages/package_table_component.html',context)

 


# package detail forms
@group_required('administrador','repartidor')
@staff_member_required(login_url='/')
def delivery_package_detail(request,pk):
    package = Package.objects.filter(pk=pk,is_delivery=False,state='2').first()
    context={'package':package}
    return render(request,'delivery_packages/actions/packageDetail/packageDetail.html',context) 


# Checked result table
@group_required('administrador')
@staff_member_required(login_url='/')
def delivery_package_checked(request,pk):
    package = Package.objects.filter(pk=pk,is_delivery=False,state='2').first()
    context={
        'package':package
    }
    if request.method == "POST":
        if package:
            import datetime
            package.is_delivery = True
            package.delivery_datetime = datetime.datetime.now()
            package.delivery_user_pk = request.user.pk
            package.delivery_user_username = request.user.username
            package.delivery_user_email = request.user.email
            package.save()
            context['package']=[]
            return  render(request,'delivery_packages/package_table_component.html',context)
    return  render(request,'delivery_packages/actions/packageChecked/packageCheckedVerify.html',context)