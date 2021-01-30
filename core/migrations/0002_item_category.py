# Generated by Django 2.2.13 on 2021-01-24 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('S', 'Shirt'), ('SW', 'Sportwear'), ('OW', 'Outerwear')], default='S', max_length=1),
            preserve_default=False,
        ),
    ]
