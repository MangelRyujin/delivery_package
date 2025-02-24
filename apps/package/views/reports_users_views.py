from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from apps.account.decorators import group_required
from apps.account.models import User
from apps.package.filters import DeliveryOrderFilter
from apps.package.models import Order, Package


# Reports view 
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def report_delivery_order_view(request):
    context={
        'orders': Order.objects.filter(state='3').order_by('-pk') ,
        
    }
    response= render(request,'reports_templates/reports_user_sales/reports.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Charge result table
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def delivery_order_table_results(request):
    orders = DeliveryOrderFilter(request.GET, queryset=Order.objects.filter(state='3').order_by('-pk')).qs
    context={
        'orders': orders,
        'item_total_price': sum(order.total_price for order in orders) or 0,
        'item_total_count': sum(order.total_packages for order in orders) or 0,
        
    }
    return  render(request,'reports_templates/reports_user_sales/reports_sales_results.html',context)
