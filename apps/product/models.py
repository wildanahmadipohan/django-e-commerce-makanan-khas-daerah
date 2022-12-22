from django.db import models

from django.core.files import File
from io import BytesIO
from PIL import Image

from apps.store.models import Store

# Category model
class Category(models.Model):
  name = models.CharField(max_length=255)
  slug = models.SlugField(max_length=255)
  description = models.TextField()
  ordering = models.IntegerField(default=0)
  image = models.ImageField(upload_to='uploads/categories/images', blank=True, null=True)
  thumbnail = models.ImageField(upload_to='uploads/categories/thumbnails', blank=True, null=True)

  class Meta:
    ordering = ['ordering']

  def __str__(self):
    return self.name

  def get_thumbnail(self):
    if self.thumbnail:
      return self.thumbnail.url
    else:
      if self.image:
        self.thumbnail = self.make_thumbnail(self.image)
        self.save()

        return self.thumbnail.url
      else:
        return 'https://via.placeholder.com/240x180.jpg'

  def make_thumbnail(self, image, size=(300, 200)):
    img = Image.open(image)
    img.convert('RGB')
    img.thumbnail(size)

    thumb_io = BytesIO()
    img.save(thumb_io, 'JPEG', quality=85)

    thumbnail = File(thumb_io, name=image.name)

    return thumbnail
    

# Product model
class Product(models.Model):
  category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
  store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  slug = models.SlugField(max_length=255)
  description = models.TextField()
  price = models.IntegerField()
  discount = models.IntegerField(default=0)
  discount_price = models.IntegerField(default=0)
  weight = models.IntegerField()
  stock = models.IntegerField()
  image = models.ImageField(upload_to='uploads/products/images', blank=True, null=True)
  thumbnail = models.ImageField(upload_to='uploads/products/thumbnails', blank=True, null=True)
  is_flash_sale = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return self.name

  def get_thumbnail(self):
    if self.thumbnail:
      return self.thumbnail.url
    else:
      if self.image:
        self.thumbnail = self.make_thumbnail(self.image)
        self.save()

        return self.thumbnail.url
      else:
        return 'https://via.placeholder.com/240x180.jpg'

  def make_thumbnail(self, image, size=(300, 200)):
    img = Image.open(image)
    img.convert('RGB')
    img.thumbnail(size)

    thumb_io = BytesIO()
    img.save(thumb_io, 'JPEG', quality=85)

    thumbnail = File(thumb_io, name=image.name)

    return thumbnail

class ProductImage(models.Model):
  product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
  image = models.ImageField(upload_to='uploads/products/images', blank=True, null=True)
  thumbnail = models.ImageField(upload_to='uploads/products/thumbnails', blank=True, null=True)

  def get_thumbnail(self):
    if self.thumbnail:
      return self.thumbnail.url
    else:
      if self.image:
        self.thumbnail = self.make_thumbnail(self.image)
        self.save()

        return self.thumbnail.url
      else:
        return 'https://via.placeholder.com/240x180.jpg'

  def make_thumbnail(self, image, size=(300, 200)):
    img = Image.open(image)
    img.convert('RGB')
    img.thumbnail(size)

    thumb_io = BytesIO()
    img.save(thumb_io, 'JPEG', quality=85)

    thumbnail = File(thumb_io, name=image.name)

    return thumbnail