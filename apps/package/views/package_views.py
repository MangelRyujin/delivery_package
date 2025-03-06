from apps.account.models import User, UserGallery
from apps.package.filters import PackageFilter
from apps.package.forms.package_forms import CreateImagePackageForm, CreateUserGalleryForm, PackageForm, UpdatePackageForm
from apps.package.models import ImagePackage, Package,Customer,Addressee
from django.shortcuts import render,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
import logging
from django.forms import modelformset_factory
from apps.account.decorators import group_required
from utils.paginator import _create_paginator
logger = logging.getLogger(__name__)
from django.db.models import Q
from django.utils.translation import gettext as _
  
# packages index 
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def packages_view(request):
    context=_show_packages(request)
    context['form']  = PackageForm()
    context['user_images']  = UserGallery.objects.filter(user=request.user)
    context['image_form']= CreateUserGalleryForm()
    context['customers']  = Customer.objects.all()
    response= render(request,'packages/package.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# packages search result
@staff_member_required(login_url='/')
def packages_results_view(request):
    return  render(request,'packages/package_result.html',context=_show_packages(request))
 
 # orders search funtion
@staff_member_required(login_url='/')
def _show_packages(request):
    return _create_paginator(request,PackageFilter(request.GET, queryset=Package.objects.all().order_by('state','-pk')))
    

# package detail forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_component_table_detail(request,pk):
    package = Package.objects.filter(pk=pk).first()
    context={'package':package}
    return render(request,'packages/package_table_component.html',context) 


# package detail forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_detail(request,pk):
    package = Package.objects.filter(pk=pk).first()
    context={'package':package}
    return render(request,'packages/actions/packageDetail/packageDetail.html',context) 


# package get addressee forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_get_addressee(request):
    customer =request.GET.get('customer',None) 
    addressees = Addressee.objects.filter(customer=customer).order_by('full_name') if customer  else []
    context={'addressees':addressees}
    return render(request,'packages/actions/getAddressee/selectOptions.html',context) 

# package get addressee forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_get_addressee_update(request,pk):
    package= Package.objects.filter(pk=pk).first()
    customer = request.GET.get('customer',None) 
    addressees = Addressee.objects.filter(customer=customer).order_by('full_name') if customer  else []
    context={
        'addressees':addressees,
        'package':package
        }
    return render(request,'packages/actions/getAddressee/selectOptions.html',context) 

# package detail forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_create(request):
    form = PackageForm()
    user_images = UserGallery.objects.filter(user=request.user)
    context={
        'form' : form,
        'customers' : Customer.objects.all(),
        'image_form' : CreateUserGalleryForm(),
        'user_images' : user_images,
        }
    if request.method == "POST":
        import datetime 
        form = PackageForm(request.POST,request.FILES)
        payment_confirm = request.POST.get('payment_confirm', None)
        if form.is_valid():                
            package = form.save()
            if payment_confirm:
                package.payment_state='2'
                package.payment_datetime = datetime.datetime.now()
                package.save()
            for image in user_images:
                package_image = ImagePackage.objects.create(
                    package = package,
                    image = image.image
                )
                package_image.save()
                image.delete()
            context['message']='Paquete creado correctamente'
        else:
            context['message']='Corrija los errores'
    context['user_images']=[]
    return render(request,'packages/actions/packageCreate/packageCreateForm.html',context) 


# package update forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def userGallery_create(request):
    image_form = CreateUserGalleryForm()
    if request.method == "POST":
        image_form = CreateUserGalleryForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.save(commit=False)
            image.user=request.user
            image.save()
    context = {
        'user_images' : UserGallery.objects.filter(user=request.user),
        'image_form' : image_form
        }
    return render(request,'packages/actions/packageCreate/imagePackage.html',context) 

# package update forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def userGallery_delete(request,pk):
    image = UserGallery.objects.filter(pk=pk).first()
    if request.method == "POST":
        if image:
            image.delete()
    context = {
        'user_images' : UserGallery.objects.filter(user=request.user),
        'image_form' : CreateUserGalleryForm()
        }
    return render(request,'packages/actions/packageCreate/imagePackage.html',context) 


# package update forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_update(request,pk):
    package = Package.objects.filter(pk=pk).first()
    context={
        'form':UpdatePackageForm(instance=package),
        'package':package,
        'customers':Customer.objects.all(),
        'addressees':Addressee.objects.filter(customer=package.customer),
        'image_form' : CreateImagePackageForm()
        
        }        
    return render(request,'packages/actions/packageUpdate/packageUpdateForm.html',context) 

# package information form
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_information_update(request,pk):
    package = Package.objects.filter(pk=pk).first()
    form = UpdatePackageForm(instance=package)
    context={
        'form':form,
        'package':package,
        'customers':Customer.objects.all(),
        'addressees':Addressee.objects.filter(customer=package.customer),
        'image_form' : CreateImagePackageForm()
        }
    if request.method == "POST":
        form = UpdatePackageForm(request.POST,instance = package)
        if form.is_valid():
            form.save()
            payment_state=request.POST.get('payment_confirm','')
            if payment_state:
                package.payment_state = '2'
            else:
                package.payment_state = '1'
            package.save()
            context['form']=form
            context['message']= "Editado correctamente" 
    return render(request,'packages/actions/packageUpdate/packageUpdateForm.html',context) 


# package images form
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_images_update(request,pk):
    package = Package.objects.filter(pk=pk).first()
    form = CreateImagePackageForm(instance=package)
    context={
        'image_form':form,
        'package':package,
        }
    if request.method == "POST":
        form = CreateImagePackageForm(request.POST,request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.package = package
            image.save()
            context['image_form']=form
            context['message']= "Imagen añadida correctamente" 
        else:
            print(form.errors)
    return render(request,'packages/actions/packageUpdate/imagesForm.html',context) 

# package images form
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_payment_update(request,pk):
    import datetime
    package = Package.objects.filter(pk=pk).first()
    context={}
    if request.method == 'POST':
        if package.payment_state == '1':
            package.payment_state = '2'
            package.payment_method = request.POST['payment_method'] or '1'
            package.payment_datetime = datetime.datetime.now()
            
            context['message']= "Se ha pagado"
        else:
            package.payment_state = '1'
            package.payment_datetime = None
            
            context['message']= "No se ha pagado"
        package.save()
    context['package']= package
    return render(request,'packages/actions/packageUpdate/paymentForm.html',context) 


# package images form
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_images_delete(request,pk):
    image = ImagePackage.objects.filter(pk=pk).first()
    package = image.package
    form = CreateImagePackageForm(instance=package)
    context={
        'image_form':form,
        'package':package,
        }
    if request.method == "POST":
        image.delete()
    return render(request,'packages/actions/packageUpdate/imagesForm.html',context) 




# Delete result table
@group_required('administrador')
@staff_member_required(login_url='/')
def package_delete(request,pk):
    package = Package.objects.filter(pk=pk).first()
    context={
        'package':package
    }
    if request.method == "POST":
        if package:
            package.delete()
            context['package']=[]
            return  render(request,'packages/package_table_component.html',context)
    return  render(request,'packages/actions/packageDelete/packageDeleteVerify.html',context)

# package detail forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_component_table_payment(request,pk):
    package = Package.objects.filter(pk=pk).first()
    context  = {
        'package':package
    }
    if package.payment_state == '2' and package.bulk > 0:
        package.state='2'
        package.save()
        
    return render(request,'packages/package_table_component.html',context) 

# package detail forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_component_table_delivery(request,pk):
    package = Package.objects.filter(pk=pk).first()
    context  = {
        'package':package
    }
    if package.state == '2':
        package.state='3'
        package.is_delivery = True
        package.save()
        
    return render(request,'packages/package_table_component.html',context) 