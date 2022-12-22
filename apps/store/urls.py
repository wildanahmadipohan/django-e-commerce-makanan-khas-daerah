from django.urls import path

from . import views

urlpatterns = [
  path('seller/products/', views.products, name='seller_products'),
  path('seller/orders/', views.orders, name='seller_orders'),
  path('seller/edit-product/<int:id>/', views.edit_product, name='seller_edit_product'),
  path('seller/delete-product/<int:id>/', views.delete_product, name='seller_delete_product'),
  path('seller/add-product/', views.add_product, name='seller_add_product'),
  path('seller/setting/profile/', views.profile, name='seller_profile_setting'),
  path('seller/flash_sale/', views.flash_sale, name='seller_flash_sale'),
  path('seller/flash_sale/activate/<int:id>/<str:activate>/', views.activate_flash, name='seller_activate_flash_sale'),
  path('seller/flash_sale/delete/<int:id>/', views.delete_flash, name='seller_delete_flash_sale'),
  path('seller/setting/bank-account/', views.bank_account, name='seller_bank'),
  path('orders/change-order-status/<int:order_id>/<str:status>/', views.change_order_status, name='change_order_status'),
  path('seller/', views.dashboard, name='seller_dashboard'),
  path('store/<slug:store_slug>/', views.profile_store, name='profile_store'),
]