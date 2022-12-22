from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
  user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
  gender = models.CharField(
    max_length=20,
    choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')], blank=True, null=True
  )
  birthday = models.DateField(blank=True, null=True)
  phone = models.CharField(max_length=12, blank=True, null=True)
  image = models.ImageField(upload_to='uploads/accounts/images', blank=True, null=True)

  def __str__(self):
    return self.user.username

class Address(models.Model):
  user = models.ForeignKey(User, related_name='address', on_delete=models.CASCADE)
  full_name = models.CharField(max_length=255)
  phone = models.CharField(max_length=50)
  province_id = models.CharField(max_length=30)
  province = models.CharField(max_length=100)
  city_id = models.CharField(max_length=30)
  city = models.CharField(max_length=100)
  postal_code = models.CharField(max_length=20)
  street = models.CharField(max_length=255)
  detail_address = models.CharField(max_length=255, blank=True, null=True)
  isMainAddress = models.BooleanField(default=False)

  class Meta:
    ordering = ['-isMainAddress']

  def __str__(self):
    return self.user.username