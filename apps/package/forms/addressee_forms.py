from django import forms

from apps.package.models import Addressee

# from apps.accounts.models import Profile

class AddresseeForm(forms.ModelForm):
    
    class Meta:
        model = Addressee
        fields = '__all__'