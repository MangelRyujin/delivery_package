from apps.account.models import User
import django_filters
from apps.package.models import Addressee, Customer
  

class CustomerFilter(django_filters.FilterSet):
    email=  django_filters.CharFilter(lookup_expr='icontains')
    full_name=  django_filters.CharFilter(lookup_expr='icontains')
    dni=  django_filters.CharFilter(lookup_expr='icontains')
    phone_number=  django_filters.CharFilter(lookup_expr='icontains')
    address=  django_filters.CharFilter(lookup_expr='icontains')

    
    class Meta:
        model = Customer
        fields = ['email','full_name','dni','phone_number','email','address']
        


class AddresseeFilter(django_filters.FilterSet):
    customer_email = django_filters.CharFilter(field_name='customer__email', lookup_expr='icontains')
    email=  django_filters.CharFilter(lookup_expr='icontains')
    full_name=  django_filters.CharFilter(lookup_expr='icontains')
    dni=  django_filters.CharFilter(lookup_expr='icontains')
    phone_number=  django_filters.CharFilter(lookup_expr='icontains')
    address=  django_filters.CharFilter(lookup_expr='icontains')

    
    class Meta:
        model = Addressee
        fields = ['email','full_name','dni','phone_number','email','address']
        
