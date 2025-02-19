from django.contrib import admin

from apps.package.models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Addressee)


class ImagePackageInline(admin.TabularInline):
    model = ImagePackage
    extra = 0

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'customer', 'addressee','cost', 'tax','weight','state','created_at','payment_state','payment_method']
    list_per_page = 200
    inlines = [ImagePackageInline,]