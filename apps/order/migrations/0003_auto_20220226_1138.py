# Generated by Django 3.2 on 2022-02-26 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_store_postal_code'),
        ('order', '0002_auto_20220223_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='store',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='user_paid',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_code',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shiping_method',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shiping_receipt',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Belum Bayar', 'Belum Bayar'), ('Dikemas', 'Dikemas'), ('Dikirim', 'Dikirim'), ('Selesai', 'Selesai')], default='Belum Bayar', max_length=50),
        ),
        migrations.RemoveField(
            model_name='order',
            name='store',
        ),
        migrations.AddField(
            model_name='order',
            name='store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='store.store'),
            preserve_default=False,
        ),
    ]
