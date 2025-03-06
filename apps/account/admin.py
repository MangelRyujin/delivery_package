from django.contrib import admin

from apps.account.models import User,UserGallery

# Register your models here.

admin.site.register(User)
admin.site.register(UserGallery)