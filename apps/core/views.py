from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.core.models import FlashSale

import datetime

from apps.store.models import Store
from apps.product.models import Product
from apps.account.models import Account

def landingpage(request):
  products = Product.objects.all()

  today = datetime.datetime.now().date()
  number_session = get_number_session()

  flash_product_today = FlashSale.objects.filter(flash_date=today, is_active=True, session_number=number_session)[:4]

  return render(request, 'core/landingpage.html', {'products': products, 'flash_product_today': flash_product_today, 'number_session': number_session})


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

def register_view(request):
  form = UserCreationForm(request.POST or None)
  
  if request.method == 'POST':

    if form.is_valid():
      user = form.save()

      login(request, user)

      store = Store.objects.create(name=user.username, owner=user)
      account = Account.objects.create(user=user)

      return redirect('landingpage')
    
  return render(request, 'core/register.html', {'form': form})

# def login_view(request):
#   if request.user.is_authenticated:
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#   if request.method == 'POST':
#     form = AuthenticationForm(data=request.POST)
#     if form.is_valid():
#       user = form.get_user()
#       login(request, user)

#       if 'next' in request.POST:
#         return redirect(request.POST.get('next'))
      
#       return redirect('landingpage')
#   else:
#     form = AuthenticationForm()

#   return render(request, 'core/login.html', {'form': form})