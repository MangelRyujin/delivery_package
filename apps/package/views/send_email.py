from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.package.models import Addressee, Customer
from utils.send_email import send_email_to_customer

# Reports view 
@staff_member_required(login_url='/')
def send_email_view(request):
   context={}
   if request.POST:
      # send_email_to_customer(customer)
      context['message']="email enviado"
   # return render(request,'send_email.html',context)
   return render(request,'email/orders__send.html',context)


def validate_addressee_orders_view(request):
   context={}
   if request.POST:
      code= request.POST['code']
      customer = Customer.objects.filter(pk = code).first()
      if customer:
         context['message']=f"Bienvenido {customer.full_name}"
      else:
         context['error']="No existe el cliente"
   return render(request,'addressee_orders/addressee_orders.html',context)

