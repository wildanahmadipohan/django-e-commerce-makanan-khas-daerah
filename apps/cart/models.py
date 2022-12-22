from itertools import product
from django.db import models
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from apps.core.models import FlashSale
from apps.order.utilities import isProductFlashSale
from apps.product.models import Product

class Cart(models.Model):
  user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username

  @property
  def get_cart_total(self):
    cartitems = self.cartdetail_set.all()
    total = sum([item.get_total for item in cartitems])
    return total
  
  @property
  def get_cart_items(self):
    cartitems = self.cartdetail_set.all()
    total = sum([item.qty for item in cartitems])
    return total

class CartDetail(models.Model):
  cart = models.ForeignKey(Cart, blank=True, null=True, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
  qty = models.IntegerField(default=0, blank=True, null=True,)
  date_added = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-date_added']

  def __str__(self):
    return self.cart.user.username

  @property
  def get_total(self):
    flash_sale = isProductFlashSale(self.product)
    if flash_sale:
      total = self.product.discount_price * self.qty
      return total
      
    total = self.product.price * self.qty
    return total