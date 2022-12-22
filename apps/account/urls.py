from django.urls import path

from . import views

urlpatterns = [
  path('profile/', views.profile, name='profile'),
  path('address/', views.address, name='address'),
  path('get_address/<int:id>', views.get_address, name='get_address'),
  path('delete_address/<int:id>', views.delete_address, name='delete_address'),
  path('edit_address/<int:id>', views.edit_address, name='edit_address'),
  path('orders/', views.orders, name='orders'),
]