# Generated by Django 2.2.13 on 2021-02-05 22:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0014_auto_20210201_0750'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BillingAddress',
            new_name='Address',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='billing_address',
            new_name='address',
        ),
    ]
