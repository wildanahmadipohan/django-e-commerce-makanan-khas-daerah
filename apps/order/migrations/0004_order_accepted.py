# Generated by Django 3.2 on 2022-03-12 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20220226_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]