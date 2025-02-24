from django import forms

from apps.package.models import Customer

# from apps.accounts.models import Profile

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        exclude = ['delivery_code']