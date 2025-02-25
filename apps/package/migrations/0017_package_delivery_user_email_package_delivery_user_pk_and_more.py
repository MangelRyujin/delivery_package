# Generated by Django 4.2 on 2025-02-25 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0016_package_is_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='delivery_user_email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='delivery_user_pk',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='delivery_user_username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
