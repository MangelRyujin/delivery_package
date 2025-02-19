# Generated by Django 4.2 on 2025-02-19 03:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0004_alter_addressee_address_alter_addressee_full_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('weight', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('tax', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('message', models.TextField(blank=True, null=True)),
                ('state', models.CharField(choices=[('1', 'procesando'), ('2', 'completado')], default='1', max_length=1)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('payment_state', models.CharField(choices=[('1', 'pendiente'), ('2', 'pagado')], default='1', max_length=1)),
                ('payment_method', models.CharField(choices=[('1', 'en proceso'), ('2', 'transferencia'), ('3', 'tarjeta')], default='1', max_length=1)),
                ('payment_datetime', models.DateTimeField()),
                ('addressee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addressee_package', to='package.addressee')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custommer_package', to='package.customer')),
            ],
            options={
                'verbose_name': 'Package',
                'verbose_name_plural': 'Packages',
            },
        ),
        migrations.CreateModel(
            name='ImagePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='image_package/')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_package', to='package.package')),
            ],
            options={
                'verbose_name': 'Image Package',
                'verbose_name_plural': 'Images Package',
            },
        ),
    ]
