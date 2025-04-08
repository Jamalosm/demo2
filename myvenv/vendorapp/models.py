from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    business_info = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    warranty_period = models.IntegerField(help_text="Warranty period in months")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    warranty_expiry = models.DateField()

    def save(self, *args, **kwargs):
        self.warranty_expiry = self.purchase_date + timedelta(days=self.product.warranty_period * 30)
        super().save(*args, **kwargs)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    products = models.ManyToManyField(ProductRegistration)  # ✅ Fixed ManyToManyField issue
    invoice_file = models.FileField(upload_to="invoices/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.customer.user.username}"
