# Generated by Django 3.2 on 2022-02-23 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_store_postal_code'),
        ('product', '0003_alter_product_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user_paid',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='total_price',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.store'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='user_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='order',
            name='store',
        ),
        migrations.AddField(
            model_name='order',
            name='store',
            field=models.ManyToManyField(related_name='orders', to='store.Store'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='product.product'),
        ),
    ]