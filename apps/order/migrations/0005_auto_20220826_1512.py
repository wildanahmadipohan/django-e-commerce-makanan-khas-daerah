# Generated by Django 3.2 on 2022-08-26 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_accepted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address',
            new_name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='order',
            name='regency',
        ),
        migrations.AddField(
            model_name='order',
            name='city_id',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='detail_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='province_id',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='street',
            field=models.CharField(default='Nama Jalan', max_length=255),
            preserve_default=False,
        ),
    ]