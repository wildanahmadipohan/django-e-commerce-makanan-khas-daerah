from django.urls import path

from . import views

urlpatterns = [
  path('accepted/<int:order_id>/', views.accepted, name='order_accepted'),
  path('couriers/<int:origin>/<int:destination>/<int:weight>/', views.couriers, name='couriers'),
  path('checkout/', views.chechkout, name='checkout'),
]