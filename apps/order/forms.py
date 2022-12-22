from django import forms

from apps.order.models import Order

class OrderForm(forms.Form):
  full_name = forms.CharField(max_length=100, label='Nama Lengkap', widget=forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Nama Lengkap'
  }))

  phone = forms.CharField(max_length=100, label='Nomor Telepon', widget=forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Nomor Telepon'
  }))

  address = forms.CharField(max_length=100, label='Alamat Lengkap', widget=forms.Textarea(attrs={
    'class': 'form-control',
    'rows': 4
  }))
  
  province = forms.CharField(widget=forms.HiddenInput())

  regency = forms.CharField(widget=forms.HiddenInput())

class ConfirmPaymentForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = ['payment_proof']

[
  {
    'code': 'jne',
    'name': 'Jalur Nugraha Ekakurir (JNE)',
    'costs': [
      {
        'service': 'OKE',
        'description': 'Ongkos Kirim Ekonomis',
        'cost': [
          {
            'value': 52000,
            'etd': '4-5',
            'note': ''
          }
        ]
      },
      {
        'service': 'REG',
        'description': 'Layanan Reguler',
        'cost': [
          {
            'value': 56000,
            'etd': '2-3',
            'note': ''
          }
        ]
      }
    ]
  }
]





[
  {
    'name': 'POS Indonesia (POS)',
    'values': [
      {
        'service': 'Pos Reguler',
        'description': 'Pos Reguler',
        'cost': [
          {
            'value': 33000,
            'etd': '5 HARI',
            'note': ''
          }
        ]
      }
    ]
  },
  {
    'name': 'Citra Van Titipan Kilat (TIKI)',
    'values': [
      {
        'service': 'ECO',
        'description': 'Economy Service',
        'cost': [
          {
            'value': 35500,
            'etd': '4',
            'note': ''
          }
        ]
      },
      {
        'service': 'REG',
        'description': 'Regular Service',
        'cost': [
          {
            'value': 38500,
            'etd': '3',
            'note': ''
          }
        ]
      }
    ]
  }
]