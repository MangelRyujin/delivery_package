from django import forms

from apps.package.models import ImagePackage, Order, Package

# from apps.accounts.models import Profile

class PackageForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False,)
    class Meta:
        model = Package
        fields = ['customer','addressee','cost','weight','bulk','tax','message','type','images','payment_method']


class UpdatePackageForm(forms.ModelForm):
    
    class Meta:
        model = Package
        fields = ['customer','addressee','cost','weight','bulk','tax','type','message']
 
        
class CreateImagePackageForm(forms.ModelForm):
    
    class Meta:
        model = ImagePackage
        fields = ['image']



class CreateOrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['sent_date','delivery_date','packages']

class UpdateOrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        exclude = ['type']