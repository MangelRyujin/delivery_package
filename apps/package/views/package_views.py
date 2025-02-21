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
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def packages_view(request):
    packages = Package.objects.filter(state='1').order_by('-id')
    context = {
        'packages':packages,
        'form': PackageForm(),
        'customers':Customer.objects.all(),
        
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


# package detail forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_component_table_detail(request,pk):
    package = Package.objects.filter(pk=pk,state='1').first()
    context={'package':package}
    return render(request,'packages/package_table_component.html',context) 


# package detail forms
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def package_detail(request,pk):
    package = Package.objects.filter(pk=pk,state='1').first()
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
    context={
        'form':form,
        'customers':Customer.objects.all(),
        
        }
    if request.method == "POST":
        form = PackageForm(request.POST,request.FILES)
        if form.is_valid():
            package = form.save()
            if request.FILES.getlist('images'):
                for image_file in request.FILES.getlist('images'):
                    ImagePackage.objects.create(
                        package=package,
                        image=image_file
                    )
            context['message']='Paquete creado correctamente'
        else:
            context['message']='Corrija los errores'
            print(form.errors)
    return render(request,'packages/actions/packageCreate/packageCreateForm.html',context) 

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
    package = Package.objects.filter(pk=pk).first()
    context={}
    if package.payment_state == '1':
        package.payment_state = '2'
        context['message']= "Se ha pagado"
    else:
        package.payment_state = '1'
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
def package_component_table_detail(request,pk):
    package = Package.objects.filter(pk=pk,state='1').first()
    package.state='2'
    package.save()
    context={'package':[]}
    return render(request,'packages/package_table_component.html',context) 