from django.db import models

from apps.product.models import Product
from apps.store.models import Store

# Create your models here.
class FlashSale(models.Model):
  product = models.ForeignKey(Product, related_name='flash_products', on_delete=models.DO_NOTHING)
  store=models.ForeignKey(Store, related_name='flash_products', on_delete=models.DO_NOTHING)
  flash_date = models.DateField()
  session_number = models.IntegerField()
  is_active = models.BooleanField(default=False)

  def __str__(self):
    return str(self.id)