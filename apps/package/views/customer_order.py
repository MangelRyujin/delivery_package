from apps.package.models import  Customer, Order, Package
from django.shortcuts import render,get_object_or_404
import logging
logger = logging.getLogger(__name__)
  
# orders index 
def customer_orders_view(request):
    delivery_code = request.GET.get('delivery_code', '')
    customer = get_object_or_404(Customer,delivery_code=delivery_code)
    packages = Package.objects.filter(is_delivery=False,customer=customer).order_by('-id')
    context = {
            'packages':packages,
        }
    response= render(request,'customer_orders/customer_orders_result.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
    

def customer_package_detail(request,pk):
    package = Package.objects.filter(pk=pk).first()
    context={'package':package}
    return render(request,'customer_orders/packageDetail/packageDetail.html',context) 