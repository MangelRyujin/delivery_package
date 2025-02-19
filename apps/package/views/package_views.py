from apps.package.models import Package
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
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def packages_view(request):
    packages = Package.objects.filter(state='1').order_by('-id')
    context = {
        'packages':packages
        }
    response= render(request,'packages/package.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# packages search result
@staff_member_required(login_url='/')
def packages_results_view(request):
    return  render(request,'packages/package_result.html',context=_show_packages(request))
       
# packages search funtion
@staff_member_required(login_url='/')
def _show_packages(request):
    keyword = request.session.get('keyword', '')
    
    if request.method == 'POST':
        keyword = request.POST.get("keyword",'')
        request.session['keyword'] = keyword

    packages = Package.objects.filter(
        Q(pk__icontains=keyword) | Q(customer__email__icontains=keyword) |
        Q(customer__full_name__icontains=keyword) | Q(customer__phone_number__icontains=keyword) |
        Q(addressee__full_name__icontains=keyword) | Q(addressee__province__icontains=keyword)|
        Q(addressee__municipe__icontains=keyword) | Q(addressee__address__icontains=keyword)|
        Q(addressee__phone_number__icontains=keyword) ,state='1'
        ).distinct().order_by('-id')
    context={
        'packages':packages,
        
    }
    return context

