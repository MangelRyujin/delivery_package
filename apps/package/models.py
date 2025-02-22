from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Customer(models.Model):
    full_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20,null=False,blank=False)
    address=models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.full_name

    
class Addressee(models.Model):
    full_name = models.CharField(max_length=120)
    province = models.CharField(max_length=20)
    municipe = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    address=models.CharField(max_length=150)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='custommer_addressee')
    
    class Meta:
        verbose_name = "Addressee"
        verbose_name_plural = "Addressees"

    def __str__(self):
        return self.full_name
    
    


    
    
class Package(models.Model):
    PAYMENT_STATE=(
        ('1','pendiente'),
        ('2','pagado'),
    )
    STATE=(
        ('1','en proceso'),
        ('2','completado'),
        
    )
    PAYMENT_METHOD=(
        ('1','efectivo'),
        ('2','transferencia'),
        ('3','tarjeta'),
    )
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='custommer_package')
    addressee = models.ForeignKey(Addressee,on_delete=models.CASCADE,related_name='addressee_package')
    cost = models.FloatField(validators=[MinValueValidator(0)])
    weight = models.FloatField(validators=[MinValueValidator(0)])
    tax = models.FloatField(validators=[MinValueValidator(0)])
    message = models.TextField(null=True,blank=True)
    state = models.CharField(max_length=1, choices=STATE,default='1')
    created_at= models.DateTimeField(auto_now=True)
    payment_state = models.CharField(max_length=1, choices=PAYMENT_STATE,default='1')
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD,default='1')
    payment_datetime= models.DateTimeField(auto_now=False,null=True,blank=True)
    
    
    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"

    def __str__(self):
        return f"{self.pk}"
    
    @property
    def total_price(self):
        return round(self.cost - self.tax,2)
    
class ImagePackage(models.Model):
    package = models.ForeignKey(Package,on_delete=models.CASCADE,related_name='image_package')
    image = models.ImageField(upload_to='image_package/')
    
    
    class Meta:
        verbose_name = "Image Package"
        verbose_name_plural = "Images Package"

    def __str__(self):
        return f"{self.pk}"
    

class Order(models.Model):
    STATE=(
        ('1','gestionando'),
        ('2','completado'),
        ('3','en camino'),
        ('4','entregado'),
    )
    state = models.CharField(max_length=1, choices=STATE,default='1')
    sent_date= models.DateField(auto_now=False,null=True,blank=True)
    delivery_date= models.DateField(auto_now=False,null=True,blank=True)
    packages = models.ManyToManyField(Package,blank=True,related_name='orders')
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.pk}"
    
    @property
    def total_price(self):
        return round(sum(package.total_price for package in self.packages.all()) or 0 ,2)
    
    @property
    def total_packages(self):
        return self.packages.all().count()
    
    @property
    def bg_proccess(self):
        if self.state == '1':
            return 'list-group-item-warning '
        elif self.state == '2':
            return 'list-group-item-success '
        elif self.state == '3':
            return 'list-group-item-info '
        else: 
            return 'list-group-item-primary'
        