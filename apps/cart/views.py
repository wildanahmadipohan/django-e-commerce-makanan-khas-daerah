from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import json
import http.client

from apps.core.models import FlashSale
from apps.order.utilities import isProductFlashSale

from .models import Cart, CartDetail
from apps.product.models import Product

@login_required()
def cart(request):
  user = request.user
  cart, created = Cart.objects.get_or_create(user=user)
  items = cart.cartdetail_set.all()

  for item in items:
    flash_sale = isProductFlashSale(item.product)
    if flash_sale:
      item.is_flash_sale = True
    else:
      item.is_flash_sale = False

  return render(request, 'cart/cart.html', {'items': items, 'cart': cart})

def update_cart(request):
  data = json.loads(request.body)
  productId = data['productId']
  action = data['action']
  dataFrom = data['dataFrom']
  qty = data['qty']
  
  user = request.user
  product = Product.objects.get(id=productId)
  cart, created = Cart.objects.get_or_create(user=user)

  cartDetail, created = CartDetail.objects.get_or_create(cart=cart, product=product)

  if action == 'add':
    cartDetail.qty = (cartDetail.qty + qty)
    if dataFrom != 'cart-templates':
      messages.success(request, 'Produk ditambahkan ke keranjang.')
  elif action == 'remove':
    cartDetail.qty = (cartDetail.qty - 1)

  cartDetail.save()

  if action == 'delete':
    cartDetail.delete()

  if cartDetail.qty <= 0:
    cartDetail.delete()

  return JsonResponse('Item was added', safe=False)

def delete_cart(request):

  user = request.user
  cart = Cart.objects.get(user=user)
  cart.delete()

  return JsonResponse('Cart was deleted', safe=False)

# get province
def get_provinces(request):
  conn = http.client.HTTPSConnection("api.rajaongkir.com")

  headers = { 'key': "96984e7432ac78357184e4f8551080c3" }

  conn.request("GET", "/starter/province", headers=headers)

  res = conn.getresponse()
  data = res.read()
  dataObject = json.loads(data)
  provinces = dataObject['rajaongkir']['results']

  return JsonResponse(provinces, safe=False)

def get_cities(request):
  data = json.loads(request.body)
  provinceId = data['provinceId']

  conn = http.client.HTTPSConnection("api.rajaongkir.com")

  headers = { 'key': "96984e7432ac78357184e4f8551080c3" }

  conn.request("GET", "/starter/city?province={}".format(provinceId), headers=headers)

  res = conn.getresponse()
  data = res.read()
  dataObject = json.loads(data)
  cities = dataObject['rajaongkir']['results']

  return JsonResponse(cities, safe=False)

def get_city(request, city_id):
  conn = http.client.HTTPSConnection("api.rajaongkir.com")
  headers = { 'key': "96984e7432ac78357184e4f8551080c3" }
  conn.request("GET", "/starter/city?id={}".format(city_id), headers=headers)

  res = conn.getresponse()
  data = res.read()
  dataObject = json.loads(data)
  city = dataObject['rajaongkir']['results']

  return JsonResponse(city, safe=False)