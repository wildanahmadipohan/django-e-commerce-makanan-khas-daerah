from django.db import models

from django.contrib.auth.models import User

from apps.product.models import Product
from apps.store.models import Store

class Order(models.Model):
  full_name = models.CharField(max_length=255)
  phone = models.CharField(max_length=50)
  province_id = models.CharField(max_length=30)
  province = models.CharField(max_length=100)
  city_id = models.CharField(max_length=30)
  city = models.CharField(max_length=100)
  postal_code = models.CharField(max_length=20)
  street = models.CharField(max_length=255)
  detail_address = models.CharField(max_length=255, blank=True, null=True)
  paid_amount = models.IntegerField()
  payment_code = models.CharField(max_length=3, blank=True, null=True)
  payment_proof = models.ImageField(upload_to='uploads/payment', blank=True, null=True)

  LIST_STATUS = (
    ('Belum Bayar', 'Belum Bayar'),
    ('Dikemas', 'Dikemas'),
    ('Dikirim', 'Dikirim'),
    ('Selesai', 'Selesai'),
  )

  status = models.CharField(max_length=50, choices=LIST_STATUS, default='Belum Bayar')
  shiping_method = models.CharField(max_length=100)
  shiping_service = models.CharField(max_length=100)
  shiping_description = models.CharField(max_length=100)
  shiping_cost = models.IntegerField()
  shiping_receipt = models.CharField(max_length=100, blank=True, null=True)
  accepted = models.BooleanField(default=False)
  user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
  store = models.ForeignKey(Store, related_name='orders', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return self.user.username
    

class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  
  product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
  price = models.IntegerField()
  qty = models.IntegerField(default=1)
   
  def __str__(self):
    return self.product.name

  def get_total_price(self):
    return self.price * self.qty
