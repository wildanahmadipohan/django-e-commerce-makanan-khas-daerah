from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from apps.core.models import FlashSale

from apps.product.models import Product
from apps.store.models import Store

from .forms import ProductForm, ShipingForm, StoreProfileForm, StoreBankAccountForm, ProductImageForm

from apps.order.models import Order

import datetime


def profile_store(request, store_slug):
  store = get_object_or_404(Store, slug=store_slug)
  products = store.products.all()

  store.regency = store.regency.split('-')[1]
  store.province = store.province.split('-')[1]

  return render(request, 'store/store.html', {'store': store, 'products': products})


@login_required
def dashboard(request):
  store = request.user.store

  order_count = {
    'paidCount' : store.orders.filter(status='Belum Bayar').count(),
    'packingCount' : store.orders.filter(status='Dikemas').count(),
    'shipingCount' : store.orders.filter(status='Dikirim').count(),
    'doneCount' : store.orders.filter(status='Selesai').count()
  }

  return render(request, 'store/dashboard.html', {'store': store, 'order_count' : order_count})

@login_required
def products(request):
  store = request.user.store
  products = store.products.all()

  return render(request, 'store/products.html', {'store': store, 'products': products})

@login_required
def flash_sale(request):
  store = request.user.store
  products = store.products.filter(stock__gte=3, is_flash_sale=False)
  
  today = datetime.datetime.now().date()
  flash_sale = FlashSale.objects.filter(flash_date=today, store=store)
  
  if request.method == 'POST' and request.POST.get('create-session-flash-sale'):
    session_date = request.POST.get('tanggal-sesi')
    session_number = request.POST.get('waktu-sesi')
    list_id = request.POST.getlist('select-product')
    
    products = []
    for id in list_id:
      product = store.products.get(id=id)
      products.append(product)

    return render(request, 'store/buat_flash_sale.html', {'session_date': session_date, 'session_number': session_number, 'products': products, 'list_id': list_id})

  if request.method == 'POST' and request.POST.get('create-flash-sale'):
    flash_date = datetime.datetime.strptime(request.POST.get('flash-date'), "%Y-%m-%d").date()
    session_number = request.POST.get('session-number')
    product_id = request.POST.getlist('product-id')
    price_list = request.POST.getlist('price')
    discount_list = request.POST.getlist('discount')
    discount_price_list = request.POST.getlist('discount-price')
    
    for index, id in enumerate(product_id):
      product = store.products.get(id=id)
      product.discount = discount_list[index]
      product.discount_price=discount_price_list[index]
      product.is_flash_sale = True
      product.save()

      FlashSale.objects.create(product=product, store=store, flash_date=flash_date, session_number=session_number)

  return render(request, 'store/flash_sale.html', {'products': products, 'flash_sale': flash_sale})

@login_required
def activate_flash(request, id, activate):
  flash_product = FlashSale.objects.get(id=id)
  product = Product.objects.get(id=flash_product.product.id)
  
  if activate == 'activate':
    flash_product.is_active = True
    flash_product.save()
  else:
    flash_product.is_active = False
    flash_product.save()

  return redirect('seller_flash_sale')

@login_required
def delete_flash(request, id):
  flash_product = get_object_or_404(FlashSale, id=id)
  product = get_object_or_404(Product, id=flash_product.product.id)
  
  product.is_flash_sale = False
  product.discount = 0
  product.discount_price = 0
  product.save()
  flash_product.delete()
  
  messages.success(request, 'Flash sale berhasil dihapus.')
  return redirect('seller_flash_sale') 

@login_required
def orders(request):
  store = request.user.store
  orders = store.orders.all()

  forms = ShipingForm()

  paidCount = store.orders.filter(status='Belum Bayar').count()
  packingCount = store.orders.filter(status='Dikemas').count()
  shipingCount = store.orders.filter(status='Dikirim').count()
  doneCount = store.orders.filter(status='Selesai').count()
  

  orders.paidCount = paidCount
  orders.packingCount = packingCount
  orders.shipingCount = shipingCount
  orders.doneCount = doneCount

  return render(request, 'store/orders.html', {'forms': forms, 'orders': orders})


@login_required
def add_product(request):
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES)

    if form.is_valid():
      product = form.save(commit=False)
      product.store = request.user.store
      product.slug = slugify(product.name)
      product.save()

      messages.success(request, 'Produk berhasil ditambahkan.')
      return redirect('seller_products')
    
  else:
    form = ProductForm()
  
  return render(request, 'store/add_product.html', {'form': form})

@login_required
def edit_product(request, id):
  product = get_object_or_404(Product, id=id)
  
  INITIAL = {
    'category': product.category,
    'name': product.name,
    'description': product.description,
    'price': product.price,
    'stock': product.stock,
    'image': product.image,
  }

  form = ProductForm(request.POST or None, request.FILES or None, initial=INITIAL, instance=product)
  image_form = ProductImageForm(request.POST or None, request.FILES or None)

  if request.method == 'POST':
    if image_form.is_valid():
      productimage = image_form.save(commit=False)
      productimage.product = product
      productimage.save()
      
      messages.success(request, 'Gambar Produk berhasil diperbaharui.')
      return redirect('seller_products')

    if form.is_valid():
      form.save()

      messages.success(request, 'Produk berhasil diperbaharui.')
      return redirect('seller_products')

  return render(request, 'store/edit_product.html', {'form': form, 'product': product, 'image_form': image_form})

@login_required
def delete_product(request, id):
  product = get_object_or_404(Product, id=id)
  product.delete()
  
  messages.success(request, 'Produk berhasil dihapus.')
  return redirect('seller_products') 

@login_required
def profile(request):
  store = request.user.store

  store_profile_form = StoreProfileForm(request.POST or None, request.FILES or None, initial={'nama': store.name})

  if request.method == 'POST':
    if request.POST.get('province_id') != '':
      store.province_id = request.POST.get('province_id')
      store.province = request.POST.get('province')
    if request.POST.get('city_id') != '':
      store.city_id = request.POST.get('city_id')
      store.city = request.POST.get('city')
    if request.POST.get('alamat_lengkap') != '':
      store.detail_address = request.POST.get('alamat_lengkap')
    if request.POST.get('postal_code') != '':
      store.postal_code = request.POST.get('postal_code')
    if request.POST.get('street') != '':
      store.street = request.POST.get('street')
      
    store.name = request.POST.get('nama')
    store.image = request.FILES.get('foto_profil')
    store.save()

    return redirect('seller_profile_setting')

  return render(request, 'store/profile.html', {
    'store': store,
    'store_profile_form': store_profile_form,
    })

@login_required
def bank_account(request):
  store = request.user.store

  forms = StoreBankAccountForm(request.POST or None)

  if request.method == 'POST':
    if forms.is_valid():
      store.account_number = forms.cleaned_data['account_number']
      store.account_name = forms.cleaned_data['account_name']
      store.bank_name = forms.cleaned_data['bank_name']

      store.save()

      return redirect('seller_bank')
  
  return render(request, 'store/bank_account.html', {'store': store, 'forms': forms})


@login_required
def change_order_status(request, order_id, status):
  order = get_object_or_404(Order, id=order_id)
  forms = ShipingForm(request.POST or None)

  if request.method == 'POST':
    if forms.is_valid():
      if order:
        shiping_receipt = forms.cleaned_data['shiping_receipt']
        
        order.status = status
        order.shiping_receipt = shiping_receipt
        order.save()

        return redirect('seller_orders')

  if order:
    if status == 'Dikirim':
      print(order_id, status)

    if status == 'Belum Bayar':
      if order.payment_proof:
        order.payment_proof.delete(save=True)
    
    order.status = status
    order.save()

    return redirect('seller_orders')