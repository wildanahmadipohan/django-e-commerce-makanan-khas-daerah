from itertools import product
from apps.core.models import FlashSale
from .models import Order, OrderItem
import datetime

def make_order(full_name, phone, province_id, province, city_id, city, postal_code, street, detail_address, user, order_by_store):
  orders_list = []

  for key, orders in order_by_store.items():
    order = Order.objects.create(
      full_name=full_name,
      phone=phone,
      province_id=province_id,
      province=province,
      city_id=city_id,
      city=city,
      postal_code=postal_code,
      street=street,
      detail_address=detail_address,
      paid_amount=orders['total_price'] + orders['shiping_cost'] + orders['payment_code'],
      shiping_method=orders['shiping_method'],
      shiping_service=orders['shiping_service'],
      shiping_description=orders['shiping_description'],
      shiping_cost=orders['shiping_cost'],
      payment_code=orders['payment_code'],
      user=user,
      store=orders['store']
    )
    
    for item in orders['items']:
      flash_sale = isProductFlashSale(item.product)
      if flash_sale:
        price = item.product.discount_price
      else:
        price = item.product.price

      OrderItem.objects.create(order=order, product=item.product, price=price, qty=item.qty)
      product = item.product
      product.stock -= item.qty
      product.save()

    orders_list.append(order)

  return orders_list

def isProductFlashSale(product):
  today = datetime.datetime.now().date()
  number_session = get_number_session()

  try:
      return FlashSale.objects.get(product=product, flash_date=today, is_active=True, session_number=number_session)
  except FlashSale.DoesNotExist:
      return None

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