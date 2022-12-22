from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
  name = models.CharField(max_length=255)
  slug = models.SlugField(max_length=255)
  owner = models.OneToOneField(User, related_name='store', on_delete = models.CASCADE)
  province_id = models.CharField(max_length=30, blank=True, null=True)
  province = models.CharField(max_length=100, blank=True, null=True)
  city_id = models.CharField(max_length=30, blank=True, null=True)
  city = models.CharField(max_length=100, blank=True, null=True)
  postal_code = models.CharField(max_length=20, blank=True, null=True)
  street = models.CharField(max_length=255, blank=True, null=True)
  detail_address = models.CharField(max_length=255, blank=True, null=True)
  account_number = models.CharField(max_length=50, blank=True, null=True)
  account_name = models.CharField(max_length=50, blank=True, null=True)
  bank_name = models.CharField(max_length=50, blank=True, null=True)
  image = models.ImageField(upload_to='uploads/store/images', blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    ordering = ['name']

  def __str__(self):
    return self.name
