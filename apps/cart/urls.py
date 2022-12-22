from django.urls import path

from . import views

urlpatterns = [
  path('cart/', views.cart, name='cart'),
  path('update_cart/', views.update_cart, name='update_cart'),
  path('get_provinces/', views.get_provinces, name='get_provinces'),
  path('get_cities/', views.get_cities, name='get_cities'),
  path('get_city/<int:city_id>/', views.get_city, name='get_city'),
  path('delete_cart/', views.delete_cart, name='delete_cart'),
]