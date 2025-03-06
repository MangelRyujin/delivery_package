from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator



# Create your models here.

class User(AbstractUser):
    email = models.EmailField("Email", blank=False,null=False,unique=True)
    phone_number = models.CharField("Phone number",max_length=20,null=True,blank=True)
    country = models.CharField("Country", max_length=255,null=True,blank=True)
    city = models.CharField("Country",max_length=255, null=True,blank=True)
    address = models.CharField("Address",max_length=255, null=True,blank=True)
 
    
class UserGallery(models.Model):
    image = models.ImageField(upload_to='user_image')
    user =  models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_images')

    class Meta:
        verbose_name = "Foto"
        verbose_name_plural = "Fotos"

    def __str__(self):
        return f'{self.pk}'

    