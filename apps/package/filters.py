import django_filters
from apps.package.models import Addressee, Customer, Order, Package
  

class CustomerFilter(django_filters.FilterSet):
    pk = django_filters.CharFilter(lookup_expr='icontains')
    email=  django_filters.CharFilter(lookup_expr='icontains')
    full_name=  django_filters.CharFilter(lookup_expr='icontains')
    phone_number=  django_filters.CharFilter(lookup_expr='icontains')
    address=  django_filters.CharFilter(lookup_expr='icontains')

    
    class Meta:
        model = Customer
        fields = ['pk','full_name','phone_number','email','address']
        


class AddresseeFilter(django_filters.FilterSet):
    pk = django_filters.CharFilter(lookup_expr='icontains')
    customer_email = django_filters.CharFilter(field_name='customer__email', lookup_expr='icontains')
    province=  django_filters.CharFilter(lookup_expr='icontains')
    municipe=  django_filters.CharFilter(lookup_expr='icontains')
    full_name=  django_filters.CharFilter(lookup_expr='icontains')
    phone_number=  django_filters.CharFilter(lookup_expr='icontains')
    address=  django_filters.CharFilter(lookup_expr='icontains')

    
    class Meta:
        model = Addressee
        fields = ['pk','full_name','customer_email','phone_number','address','province','municipe']
        

class PackageFilter(django_filters.FilterSet):
    pk = django_filters.CharFilter(lookup_expr='icontains')
    state=  django_filters.CharFilter(lookup_expr='exact')
    type=  django_filters.CharFilter(lookup_expr='exact')
    is_delivery = django_filters.BooleanFilter(lookup_expr='exact')
    customer = django_filters.CharFilter(field_name='customer__full_name', lookup_expr='icontains')
    addressee = django_filters.CharFilter(field_name='addressee__full_name', lookup_expr='icontains')
    
    class Meta:
        model = Package
        fields = ['pk','state','type','is_delivery','customer','addressee']


class OrderFilter(django_filters.FilterSet):
    pk = django_filters.CharFilter(lookup_expr='icontains')
    state=  django_filters.CharFilter(lookup_expr='exact')
    sent_date = django_filters.DateFromToRangeFilter()

    
    class Meta:
        model = Order
        fields = ['pk','state']
        
class DeliveryOrderFilter(django_filters.FilterSet):
    delivery_date =django_filters.DateFromToRangeFilter()

    class Meta:
        model = Order
        fields = ['delivery_date',]
        