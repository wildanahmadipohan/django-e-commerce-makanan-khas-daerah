import json
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.account.forms import AccountAddressForm

from apps.account.models import Address
from apps.core.models import FlashSale

from .models import Order
from .utilities import make_order, isProductFlashSale
from .forms import OrderForm

from apps.cart.models import Cart

@login_required
def chechkout(request):
  user = request.user
    
  account_address_form = AccountAddressForm(request.POST or None)
  cart = Cart.objects.get(user=user)
  
  items = cart.cartdetail_set.all()

  for item in items:
    flash_sale = isProductFlashSale(item.product)
    if flash_sale:
      item.is_flash_sale = True
    else:
      item.is_flash_sale = False

  order_by_store = get_order_by_store(items)
  
  for key, orders in order_by_store.items():
    for item in orders['items']:
      print(type(item.product))

  if request.method == 'POST' and request.POST.get('is-make-order'):
    shiping_address = Address.objects.get(user=user, id=request.POST.get('address-id'))

    for key, orders in order_by_store.items():
      orders['paid_amount'] = int(request.POST.get('paid_amount[{}]'.format(orders['store'].id)))
      orders['shiping_method'] = request.POST.get('shiping_method[{}]'.format(orders['store'].id))
      orders['shiping_service'] = request.POST.get('shiping_service[{}]'.format(orders['store'].id))
      orders['shiping_description'] = request.POST.get('shiping_description[{}]'.format(orders['store'].id))
      orders['shiping_cost'] = int(request.POST.get('shiping_cost[{}]'.format(orders['store'].id)))
      # print(type(orders['paid_amount']))

    full_name = shiping_address.full_name
    phone = shiping_address.phone
    province_id = shiping_address.province_id
    province = shiping_address.province
    city_id = shiping_address.city_id
    city = shiping_address.city
    postal_code = shiping_address.postal_code
    street = shiping_address.street
    detail_address = shiping_address.detail_address

    orders = make_order(full_name, phone, province_id, province, city_id, city, postal_code, street, detail_address, user, order_by_store)

    if orders:
      cart.delete()

      return render(request, 'order/success.html', {'orders': orders})

  return render(request, 'order/checkout.html', {'orders': order_by_store, 'cart': cart, 'account_address_form': account_address_form})


def couriers(request, origin, destination, weight):
  jne_courier = getShipingCost(origin, destination, weight, 'jne')
  pos_courier = getShipingCost(origin, destination, weight, 'pos')
  tiki_courier = getShipingCost(origin, destination, weight, 'tiki')

  available_courier = []

  if len(jne_courier) > 0:
    available_courier.append(
      {
        'name': 'Jalur Nugraha Ekakurir (JNE)',
        'values': jne_courier
      }
    )

  if len(pos_courier) > 0:
    available_courier.append(
      {
        'name': 'POS Indonesia (POS)',
        'values': pos_courier
      }
    )

  if len(tiki_courier) > 0:
    available_courier.append(
      {
        'name': 'Citra Van Titipan Kilat (TIKI)',
        'values': tiki_courier
      }
    )

  static_courier = [
  {
    'name': 'POS Indonesia (POS)',
    'values': [
      {
        'service': 'Pos Reguler',
        'description': 'Pos Reguler',
        'cost': [
          {
            'value': 33000,
            'etd': '5 HARI',
            'note': ''
          }
        ]
      }
    ]
  },
  {
    'name': 'Citra Van Titipan Kilat (TIKI)',
    'values': [
      {
        'service': 'ECO',
        'description': 'Economy Service',
        'cost': [
          {
            'value': 35500,
            'etd': '4',
            'note': ''
          }
        ]
      },
      {
        'service': 'REG',
        'description': 'Regular Service',
        'cost': [
          {
            'value': 38500,
            'etd': '3',
            'note': ''
          }
        ]
      }
    ]
  }
]

  return JsonResponse(available_courier, safe=False)
  # return JsonResponse(static_courier, safe=False)

def getShipingCost(origin, destination, weight, courier):
  import http.client

  conn = http.client.HTTPSConnection("api.rajaongkir.com")

  payload = "origin={}&destination={}&weight={}&courier={}".format(origin, destination, weight, courier)

  headers = {
    'key': settings.RAJA_ONGKIR_KEY,
    'content-type': "application/x-www-form-urlencoded"
  }

  conn.request("POST", "/starter/cost", payload, headers)

  res = conn.getresponse()
  data = res.read()
  dataObject = json.loads(data)
  result = dataObject['rajaongkir']['results'][0]['costs']
  return result


@login_required
def accepted(request, order_id):
  print(order_id)
  order = get_object_or_404(Order, id=order_id)
  order.accepted = True
  order.status = 'Selesai'
  order.save()
  
  return redirect('orders')


# private function
def get_order_by_store(items):
  stores = []
  filtered_store = []

  for item in items:
    stores.append(item.product.store.name)

  [filtered_store.append(x) for x in stores if x not in filtered_store]

  order_by_store = {}

  for item in items:
    for index, store in enumerate(filtered_store):
      if store == item.product.store.name:
        if store not in order_by_store:
          order_by_store[item.product.store.name] = {
            'total_price': item.get_total,
            'payment_code': get_latest_payment_code(index + 1),
            'store': item.product.store,
            'items': [item]
            }
        else:
          order_by_store[item.product.store.name]['items'].append(item)
          order_by_store[item.product.store.name]['total_price'] += item.get_total

  return order_by_store

def get_latest_payment_code(plus):
  try:
    lastPaymentCode = Order.objects.latest('id').payment_code

    if lastPaymentCode == '200':
      lastPaymentCode = '100'
    else:
      lastPaymentCode = int(lastPaymentCode) + plus

    return lastPaymentCode
  except Order.DoesNotExist:
    lastPaymentCode = 99 + plus
    return lastPaymentCode

  