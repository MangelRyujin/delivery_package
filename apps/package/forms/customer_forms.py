from django import forms

from apps.package.models import Customer

# from apps.accounts.models import Profile

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = '__all__'