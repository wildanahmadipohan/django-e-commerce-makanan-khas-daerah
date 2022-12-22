from django.urls import path

from . import views

urlpatterns = [
  path('search/', views.search, name='search'),
  path('products/', views.all_product, name='products'),
  path('flash_sale/', views.flash_sale, name='flash_sale'),
  path('<slug:category_slug>/<slug:product_slug>/', views.detail_product, name='detail_product'),
  path('<slug:category_slug>/', views.category, name='category'),
]