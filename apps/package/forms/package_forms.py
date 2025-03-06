from django import forms

from apps.account.models import UserGallery
from apps.package.models import ImagePackage, Order, Package

# from apps.accounts.models import Profile

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['customer','addressee','cost','weight','bulk','tax','message','type','payment_method']


class UpdatePackageForm(forms.ModelForm):
    
    class Meta:
        model = Package
        fields = ['customer','addressee','cost','weight','bulk','tax','type','message','payment_method']
 
        
class CreateImagePackageForm(forms.ModelForm):
    
    class Meta:
        model = ImagePackage
        fields = ['image']

class CreateUserGalleryForm(forms.ModelForm):
    
    class Meta:
        model = UserGallery
        fields = ['image']


class CreateOrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['sent_date','delivery_date','packages']

class UpdateOrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        exclude = ['type']