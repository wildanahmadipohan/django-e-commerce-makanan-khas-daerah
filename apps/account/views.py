from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from apps.account.forms import AccountAddressForm, AccountEditForm, UserEditForm

from django.http import JsonResponse

from apps.order.forms import ConfirmPaymentForm
from apps.order.models import Order
from .models import Account, Address

@login_required
def profile(request):
  user = request.user
  account = Account.objects.get(user=user)
  
  INITIALUSER = {
    'first_name': user.first_name,
    'last_name': user.last_name,
    'email': user.email
  }

  INITIALACCOUNT = {
    'gender': account.gender,
    'birthday': account.birthday,
    'phone': account.phone
  }

  user_edit_form = UserEditForm(request.POST or None, initial=INITIALUSER, instance=user)
  account_edit_form = AccountEditForm(request.POST or None, request.FILES or None, initial=INITIALACCOUNT, instance=account)

  if request.method == 'POST':
    if user_edit_form.is_valid() and account_edit_form.is_valid():
      user_edit_form.save(commit=False)
      account_edit_form.save()
      user_edit_form.save()

      return redirect('profile')

  return render(request, 'account/profile.html', {'user': user, 'user_edit_form': user_edit_form, 'account_edit_form': account_edit_form})

@login_required
def address(request):
  user = request.user
  address = user.address.all()

  try:
    main_address = Address.objects.get(user=user, isMainAddress=True)
  except Address.DoesNotExist:
    main_address = False

  account_address_form = AccountAddressForm(request.POST or None)

  if request.method == 'POST':
    if account_address_form.is_valid():
      address = account_address_form.save(commit=False)
      address.user = user
      
      if main_address:
        if address.isMainAddress:
          main_address.isMainAddress = False
          main_address.save()
      else:
        address.isMainAddress = True

      address.save()

      if request.POST['redirect']:
        return redirect(request.POST['redirect'])

      return redirect('address')

  return render(request, 'account/address.html', {'user': user, 'address': address, 'account_address_form': account_address_form})


@login_required
def edit_address(request, id):
  address = get_object_or_404(Address, id=id)

  account_address_form = AccountAddressForm(request.POST, instance=address)
  
  if request.method == 'POST':
    if account_address_form.is_valid():
      account_address_form.save()

      return redirect('address')
    
# for frontend (API)
def get_address(request, id = 0):
  user = request.user
  
  if id:
    address = Address.objects.filter(id=id).values()
  else:
    address = Address.objects.filter(user=user).values()
  
  if address:
    response = {'empty': False, 'address': list(address)}
  else:
    response = {'empty': True, 'address': []}

  return JsonResponse(response, safe=False)


@login_required
def delete_address(request, id):
  address = get_object_or_404(Address, id=id)
  address.delete()

  return redirect('address')

@login_required
def orders(request):
  user = request.user
  status =  request.GET.get('status', '')
  if status == '1':
    orders = user.orders.all()
  elif status == '2':
    orders = user.orders.filter(status='Belum Bayar')
  elif status == '3':
    orders = user.orders.filter(status='Dikemas')
  elif status == '4':
    orders = user.orders.filter(status='Dikirim')
  elif status == '5':
    orders = user.orders.filter(status='Selesai')
  else:
    orders = user.orders.all()

  if request.method == 'POST':
    orderId = request.POST.get('orderId')
    order = get_object_or_404(Order, id=orderId)
    forms = ConfirmPaymentForm(request.POST, request.FILES, instance=order)
    if forms.is_valid():
      forms.save()

      return redirect('orders')
  else:
    forms = ConfirmPaymentForm()

  return render(request, 'account/orders.html', {'orders': orders, 'forms': forms})

