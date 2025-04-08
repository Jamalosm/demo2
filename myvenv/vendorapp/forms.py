from django import forms
from django.contrib.auth.models import User
from .models import Product, ProductRegistration, Invoice

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    ROLE_CHOICES = [
        ("Vendor", "Vendor"),
        ("Customer", "Customer"),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)  # ✅ Add role selection

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']


class ProductForm(forms.ModelForm):
    ROLE_CHOICES = [
        ("Vendor", "Vendor"),
        ("Customer", "Customer"),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)  # ✅ Fixed placement

    class Meta:
        model = Product
        exclude = ['vendor']  # ✅ Vendor will be assigned automatically

class ProductRegistrationForm(forms.ModelForm):
    class Meta:
        model = ProductRegistration
        fields = ['product', 'purchase_date']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'products', 'invoice_file']  # ✅ Correct field names
