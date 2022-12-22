from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
  path('', views.landingpage, name='landingpage'),
  path('register/', views.register_view, name='register'),
  # path('login/', views.login_view, name='login'),
  path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='core/login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]