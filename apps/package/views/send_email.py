from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from apps.package.models import Customer


def validate_customer_orders_view(request):
   context={}
   if request.POST:
      delivery_code= request.POST['delivery_code']
      customer = Customer.objects.filter(delivery_code = delivery_code).first()
      if customer:
         return redirect(reverse('customer_orders_view') + f'?delivery_code={delivery_code}')
      else:
         context['error']="No existe el cliente"
   return render(request,'customer_orders/customer_orders.html',context)

