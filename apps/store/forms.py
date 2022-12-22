from dataclasses import fields
from pyexpat import model
from django import forms

from apps.product.models import Product, ProductImage
from apps.store.models import Store

class ProductImageForm(forms.ModelForm):
  class Meta:
    model = ProductImage
    fields = ['image']

    labels = {'image': 'Gambar Tambahan'}

    widgets = {
      'image': forms.FileInput(
        attrs={
          'class': 'form-control'
        }
      )
    }

class ProductForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ['category', 'name', 'description', 'price', 'weight', 'stock', 'image']

    labels = {
      'category': 'Kategori',
      'name': 'Nama',
      'description': 'Deskripsi',
      'price': 'Harga',
      'weight': 'Berat',
      'image': 'Gambar'
    }

    widgets = {
      'category': forms.Select(
        attrs={
          'class': 'form-control'
        }
      ),
      'name': forms.TextInput(
        attrs={
        'class': 'form-control'
        }
      ),
      'description': forms.Textarea(
        attrs={
          'class': 'form-control',
          'rows': 6
        }
      ),
      'price': forms.NumberInput(
        attrs={
          'class': 'form-control'
        }
      ),
      'weight': forms.NumberInput(
        attrs={
          'class': 'form-control',
          'min': '1'
        }
      ),
      'stock': forms.NumberInput(
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
  
class StoreProfileForm(forms.Form):
  nama = forms.CharField(required=False, max_length=100, widget=forms.TextInput(
    attrs={
      'class': 'form-control'
    }
  ))

  foto_profil = forms.ImageField(required=False, widget=forms.FileInput(
    attrs={
      'class': 'form-control'
    }
  ))

  PROVINSI = (('', 'Pilih Provinsi'),)
  KABUPATEN = (('', 'Pilih Kabupaten / Kota'),)
  
  province_id = forms.ChoiceField(label='Provinsi', required=False, choices=PROVINSI, widget=forms.Select(
    attrs={
      'class': 'form-control'
    }
  ))
  province = forms.CharField(required=False, widget=forms.TextInput(
    attrs={
      'type': 'hidden'
    }
  ))

  city_id = forms.ChoiceField(label='Kabupaten / Kota', required=False, choices=KABUPATEN, widget=forms.Select(
    attrs={
      'class': 'form-control'
    }
  ))
  city = forms.CharField(required=False, widget=forms.TextInput(
    attrs={
      'type': 'hidden'
    }
  ))

  postal_code = forms.CharField(label='Kode Pos', required=False, widget=forms.TextInput(
    attrs={
      'class': 'form-control'
    }
  ))

  street = forms.CharField(label='Jalan', required=False, widget=forms.TextInput(
    attrs={
      'class': 'form-control',
      'placeholder': 'Nama Jalan, Nomor Rumah, Gedung'
    }
  ))
  
  alamat_lengkap = forms.CharField(required=False, max_length=200, widget=forms.Textarea(
    attrs={
      'class': 'form-control',
      'rows': 4
    }
  ))

class StoreBankAccountForm(forms.Form):
  account_number = forms.CharField(label='Nomor Rekening', widget=forms.TextInput(
    attrs={
      'class': 'form-control'
    }
  ))

  account_name = forms.CharField(label='Nama Rekening', widget=forms.TextInput(
    attrs={
      'class': 'form-control'
    }
  ))

  bank_name = forms.CharField(label='Nama Bank', widget=forms.TextInput(
    attrs={
      'class': 'form-control'
    }
  ))

class ShipingForm(forms.Form):
  shiping_receipt = forms.CharField(label='Nomor Resi', widget=forms.TextInput(
    attrs={
      'class': 'form-control',
      'placeholder': 'Masukkan nomor resi'
    }
  ))