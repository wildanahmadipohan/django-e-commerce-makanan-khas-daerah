from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

import datetime
import random

from apps.core.models import FlashSale


from .models import Category, Product


# search views
def search(request):
  query = request.GET.get('query', '')
  products = Product.objects.filter(Q(name__icontains=query) | Q(description__contains=query))

  return render(request, 'product/search.html', {'products': products, 'query': query})

# detail product views
def detail_product(request, category_slug, product_slug):
  product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

  imagesstring = '{"thumbnail": "%s", "image": "%s", "id": "mainimage"},' % (product.get_thumbnail(), product.image.url)

  for image in product.images.all():
    imagesstring += ('{"thumbnail": "%s", "image": "%s", "id": "%s"},' % (image.get_thumbnail(), image.image.url, image.id))

  print(imagesstring)

  similar_products = list(product.category.products.exclude(id=product.id))

  if len(similar_products) >= 4:
    similar_products = random.sample(similar_products, 4)
  
  return render(request, 'product/product-detail.html', {'product': product, 'similar_products': similar_products, 'imagesstring': "[" + imagesstring.rstrip(',') + "]"})

# category page views
def category(request, category_slug):
  category = get_object_or_404(Category, slug=category_slug)

  return render(request, 'product/category.html', {'category': category})

# all product page views
def all_product(request):
  product_list = Product.objects.all()
  page = request.GET.get('page', 1)

  paginator = Paginator(product_list, 8)

  try:
    products = paginator.page(page)
  except PageNotAnInteger:
    products = paginator.page(1)
  except EmptyPage:
    products = paginator.page(paginator.num_pages)

  return render(request, 'product/all-product.html', {'products': products})


def flash_sale(request):
  today = datetime.datetime.now().date()
  number_session = get_number_session()

  flash_product_today = FlashSale.objects.filter(flash_date=today, is_active=True, session_number=number_session)

  for flash_product in flash_product_today:
    print(flash_product.product.id)

  return render(request, 'product/flash_sale.html', {'flash_product_today': flash_product_today, 'number_session': number_session})



def time_in_range(start, end, current):
  return start <= current <= end

def get_number_session():
  if time_in_range(datetime.time(0, 0, 0), datetime.time(12, 0, 0), datetime.datetime.now().time()):
    return 1

  if time_in_range(datetime.time(12, 0, 1), datetime.time(13, 0, 0), datetime.datetime.now().time()):
    return 2

  if time_in_range(datetime.time(13, 0, 1), datetime.time(18, 0, 0), datetime.datetime.now().time()):
    return 3

  if time_in_range(datetime.time(18, 0, 1), datetime.time(21, 0, 0), datetime.datetime.now().time()):
    return 4

  if time_in_range(datetime.time(21, 0, 1), datetime.time(23, 59, 0), datetime.datetime.now().time()):
    return 5