from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from delivery_package.settings import DOMAIN_URL

def send_email_to_customer(customer):
    if customer.email:
        asunto = f"Hola {customer.email}"
        mensaje = 'Accede a tus envíos y dales seguimiento'
        remitente = settings.EMAIL_HOST_USER
        destinatario = [customer.email]
        context= {
            'customer':customer,
            'img':f"{DOMAIN_URL}/static/assets/img/malecon_travel.jpg"
        }
        message_html = render_to_string("email/orders__send.html",context)
        send_mail(asunto, mensaje, remitente, destinatario,html_message=message_html, fail_silently=False)
   
   
def order_in_proccess_send_customer_email(order):  
    if order.state == '2':
        last_customer_pk = ''
        for package in order.packages.all():
            if last_customer_pk != package.customer.pk:
                send_email_to_customer(package.customer)
                last_customer_pk = package.customer.pk # Actualize last customer pk
                
                
def send_email_to_customer_delivery_package(customer):
    if customer.email:
        asunto = f"Hola {customer.email}"
        mensaje = 'Accede a tus envíos y dales seguimiento'
        remitente = settings.EMAIL_HOST_USER
        destinatario = [customer.email]
        message_html = render_to_string("email/delivery_package__send.html")
        send_mail(asunto, mensaje, remitente, destinatario,html_message=message_html, fail_silently=False)