# Generated by Django 2.2.13 on 2021-04-29 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20210425_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.TextField(),
        ),
    ]