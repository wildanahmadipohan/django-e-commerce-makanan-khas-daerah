# Generated by Django 3.2 on 2022-08-27 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ['-isMainAddress']},
        ),
    ]
