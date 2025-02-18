from django.db import models

# Create your models here.
class Customer(models.Model):
    full_name = models.CharField(max_length=120)
    dni=models.CharField(max_length=20,null=True,blank=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    address=models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField(unique=True)
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.full_name

    
class Addressee(models.Model):
    full_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    dni=models.CharField(max_length=20,null=True,blank=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    address=models.CharField(max_length=150,null=True,blank=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='custommer_addressee')
    
    class Meta:
        verbose_name = "Addressee"
        verbose_name_plural = "Addressees"

    def __str__(self):
        return self.full_name