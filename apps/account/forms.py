from django import forms
from django.contrib.auth.models import User

from . import models

class UserEditForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email']

    labels = {
      'first_name': 'Nama Depan',
      'last_name': 'Nama Belakang',
      'email': 'Email'
    }

    widgets = {
      'first_name': forms.TextInput(
        attrs={
          'class': 'form-control'
        }
      ),
      'last_name': forms.TextInput(
        attrs={
          'class': 'form-control'
        }
      ),
      'email': forms.EmailInput(
        attrs={
          'class': 'form-control'
        }
      ),
    }

class AccountEditForm(forms.ModelForm):
  class Meta:
    model = models.Account
    fields = ['gender', 'birthday', 'phone', 'image']

    labels = {
      'gender': 'Jenis Kelamin',
      'birthday': 'Tanggal Lahir',
      'phone': 'Nomor Telepon',
      'image': 'Foto Profil'
    }

    widgets = {
      'gender': forms.Select(
        attrs={
          'class': 'form-select',
        }
      ),
      'birthday': forms.DateInput(
        attrs={
          'class': 'form-control'
        }
      ),
      'phone': forms.TextInput(
        attrs={
          'class': 'form-control'
        }
      ),
      'image': forms.FileInput(
        attrs={
          'class': 'form-control'
        }
      )
    }

class AccountAddressForm(forms.ModelForm):
  class Meta:
    model = models.Address
    fields = ['full_name', 'phone', 'province_id', 'province', 'city_id', 'city', 'postal_code', 'street', 'detail_address', 'isMainAddress']

    labels = {
      'full_name': 'Nama Lengkap',
      'phone': 'Nomor Telepon',
      'province_id': 'Provinsi',
      'city_id': 'Kabupaten / Kota',
      'postal_code': 'Kode Pos',
      'street': 'Jalan',
      'detail_address': 'Detail Lainnya',
      'isMainAddress': 'Alamat Utama'
    }

    widgets = {
      'full_name': forms.TextInput(
        attrs={
          'class': 'form-control form-control-sm',
        }
      ),
      'phone': forms.TextInput(
        attrs={
          'class': 'form-control form-control-sm',
        }
      ),
      'province': forms.TextInput(
        attrs={
          'type': 'hidden'
        }
      ),
      'province_id': forms.Select(
        choices=[('', 'Pilih Provinsi')],
        attrs={
          'class': 'form-select form-select-sm',
        }
      ),
      'city': forms.TextInput(
        attrs={
          'type': 'hidden'
        }
      ),
      'city_id': forms.Select(
        choices=[('', 'Pilih Kabupaten / Kota')],
        attrs={
          'class': 'form-select form-select-sm',
        }
      ),
      'postal_code': forms.TextInput(
        attrs={
          'class': 'form-control form-control-sm'
        }
      ),
      'street': forms.TextInput(
        attrs={
          'class': 'form-control form-control-sm',
          'placeholder': 'Nama Jalan, Nomor Rumah, Gedung'
        }
      ),
      'detail_address': forms.TextInput(
        attrs={
          'class': 'form-control form-control-sm',
          'placeholder': '(Cth: Blok / Unit No., Patokan)'
        }
      ),
      'isMainAddress': forms.CheckboxInput(
        attrs={
          'class': 'form-check-input',
          'role': 'switch'
        }
      )
    }