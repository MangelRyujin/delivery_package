from django.db import models
from django.core.validators import MinValueValidator
import uuid


def generate_delivery_code():
    while True:
        delivery_code = str(uuid.uuid4().int)[:8]  # Trunca el UUID a 8 caracteres
        if not Customer.objects.filter(delivery_code=delivery_code).exists():
            break
    return delivery_code


# Create your models here.
class Customer(models.Model):
    full_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20,null=False,blank=False,unique=True)
    address=models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    delivery_code = models.CharField(max_length=8,null=True,blank=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.delivery_code:
            self.delivery_code = generate_delivery_code()
        super().save(*args, **kwargs)
    
class Addressee(models.Model):
    full_name = models.CharField(max_length=120)
    province = models.CharField(max_length=20)
    municipe = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20,unique=True)
    address=models.CharField(max_length=150)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='custommer_addressee')
    
    class Meta:
        verbose_name = "Destinatario"
        verbose_name_plural = "Destinatarios"

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
        ('3','entregado')
        
    )
    TYPE=(
        ('1','marítimo'),
        ('2','aéreo'),
        ('3','aéreo express')
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
    bulk = models.PositiveIntegerField(default=0)
    state = models.CharField(max_length=1, choices=STATE,default='1')
    created_at= models.DateTimeField(auto_now=True)
    is_delivery = models.BooleanField(default=False)
    type = models.CharField(max_length=1, choices=TYPE,default='1')
    payment_state = models.CharField(max_length=1, choices=PAYMENT_STATE,default='1')
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD,default='1')
    payment_datetime= models.DateTimeField(auto_now=False,null=True,blank=True)
    delivery_datetime = models.DateTimeField(auto_now=False,null=True,blank=True)
    delivery_user_pk =  models.CharField(max_length=20,null=True,blank=True)
    delivery_user_username =  models.CharField(max_length=255,null=True,blank=True )
    delivery_user_email =   models.CharField(max_length=255,null=True,blank=True )
    
    class Meta:
        verbose_name = "Paquete"
        verbose_name_plural = "Paquetes"

    def __str__(self):
        return f"{self.pk}"
    
    @property
    def total_price(self):
        return round((self.cost * self.weight) + self.tax,2)
    
    @property
    def is_completed(self):
        if self.payment_state == '2' and self.bulk !=0:
            return True
        return False
    
class ImagePackage(models.Model):
    package = models.ForeignKey(Package,on_delete=models.CASCADE,related_name='image_package')
    image = models.ImageField(upload_to='image_package/')
    
    
    class Meta:
        verbose_name = "Imágen"
        verbose_name_plural = "Imágenes"

    def __str__(self):
        return f"{self.pk}"
    

class Order(models.Model):
    STATE=(
        ('1','gestionando'),
        ('2','en camino'),
        ('3','entregado'),
    )
    TYPE=(
        ('1','marítimo'),
        ('2','aéreo'),
        ('3','aéreo express')
    )
    type = models.CharField(max_length=1, choices=TYPE,default='1')
    state = models.CharField(max_length=1, choices=STATE,default='1')
    sent_date= models.DateField(auto_now=False,null=True,blank=True)
    delivery_date= models.DateField(auto_now=False,null=True,blank=True)
    packages = models.ManyToManyField(Package,blank=True,related_name='orders')
    
    class Meta:
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"

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
            return 'list-group-item-success '
        elif self.state == '2':
            return 'list-group-item-info '
        else: 
            return 'list-group-item-primary'
        