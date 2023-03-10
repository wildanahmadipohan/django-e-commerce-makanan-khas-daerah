# Generated by Django 3.2 on 2022-08-28 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20220828_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shiping_description',
            field=models.CharField(default='JNE', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shiping_method',
            field=models.CharField(default='JNE', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shiping_service',
            field=models.CharField(default='Reguler', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='shiping_cost',
            field=models.IntegerField(),
        ),
    ]
