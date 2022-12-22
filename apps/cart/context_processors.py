from apps.cart.models import Cart, CartDetail

def cart_total_item(request):
  if request.user.is_authenticated:
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_total = cart.get_cart_items
  else:
    cart_total = 0

  return {'cart_total': cart_total}