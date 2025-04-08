from django.contrib import admin
from django.urls import path
from vendorapp.views import (
    register, user_login, user_logout, dashboard,
    product_list, add_product, register_product, upload_invoice,home,vendor_dashboard
    ,customer_dashboard
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
     path('', home, name='home'),

    # Authentication
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # Product Management
    path('products/', product_list, name='product_list'),
    path('products/add/', add_product, name='add_product'),

    # Product Registration
    path('products/register/', register_product, name='register_product'),

    # Invoice Management
    path('invoices/upload/', upload_invoice, name='upload_invoice'),
    
    path('vendor/dashboard/', vendor_dashboard, name='vendor_dashboard'),
    path('customer/dashboard/', customer_dashboard, name='customer_dashboard'),
]
