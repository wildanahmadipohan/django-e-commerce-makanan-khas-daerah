# Generated by Django 3.2 on 2022-08-27 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_store_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='regency',
            new_name='city',
        ),
        migrations.RemoveField(
            model_name='store',
            name='address',
        ),
        migrations.AddField(
            model_name='store',
            name='city_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='detail_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='province_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='street',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
