from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.timezone import now
from django.core.mail import send_mail
from datetime import timedelta
from .models import Vendor, Product, ProductRegistration, Invoice,Customer
from .forms import UserRegistrationForm, ProductForm, ProductRegistrationForm, InvoiceForm
from django.core.exceptions import PermissionDenied
# ========== 1️⃣ Home Page ==========
def home(request):
    return render(request, "home.html")

# ========== 2️⃣ User Registration & Authentication ==========
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            
            # Assign user to the selected group
            role = form.cleaned_data["role"]
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            # Auto-create Vendor or Customer profile
            if role == "Vendor":
                Vendor.objects.create(user=user, name=user.username, business_info="New Vendor")
            else:
                Customer.objects.create(user=user, phone_number="", address="")

            # Send notification email
            send_mail(
                "New User Registered",
                f"A new {role} '{user.username}' has registered.",
                "your_email@gmail.com",
                ["admin_email@gmail.com"],
                fail_silently=False,
            )

            return redirect("login")
    else:
        form = UserRegistrationForm()

    return render(request, "auth/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on user role
            if is_vendor(user):
                return redirect("vendor_dashboard")
            elif is_customer(user):
                return redirect("customer_dashboard")
            else:
                return redirect("dashboard")  # Default fallback
            
        else:
            return render(request, "auth/login.html", {"error": "Invalid username or password"})

    return render(request, "auth/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")

# ========== 3️⃣ Dashboard ==========
@login_required
def dashboard(request):
    return render(request, "dashboard.html")

# ========== 4️⃣ Product Management ==========
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})

@login_required
def add_product(request):
    vendor = Vendor.objects.filter(user=request.user).first()  # Check Vendor existence
    if not vendor:
        return render(request, "error.html", {"message": "You must be registered as a Vendor to add products."})

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor  # Assign vendor
            product.save()
            return redirect("product_list")
    else:
        form = ProductForm()

    return render(request, "products/add_products.html", {"form": form})

# ========== 5️⃣ Product Registration ==========
@login_required
def register_product(request):
    if request.method == "POST":
        form = ProductRegistrationForm(request.POST)
        if form.is_valid():
            product_registration = form.save(commit=False)
            product_registration.user = request.user
            product_registration.save()

            # Send email directly (without Celery)
            send_mail(
                subject=f"Warranty Expiry Reminder: {product_registration.product.name}",
                message=f"Your product '{product_registration.product.name}' is nearing its warranty expiry.",
                from_email="no-reply@vendorproject.com",
                recipient_list=[request.user.email],
                fail_silently=False,
            )

            return redirect("dashboard")
    else:
        form = ProductRegistrationForm()
    
    return render(request, "products/register_product.html", {"form": form})

# ========== 6️⃣ Invoice Management ==========
@login_required
def upload_invoice(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()
            return redirect("dashboard")
    else:
        form = InvoiceForm()
    
    return render(request, "invoices/upload_invoice.html", {"form": form})



def is_vendor(user):
    return user.groups.filter(name='Vendor').exists()

def is_customer(user):
    return user.groups.filter(name='Customer').exists()

@login_required
def vendor_dashboard(request):
    if request.user.groups.filter(name='Vendor').exists():
        return render(request, 'vendor_dashboard.html')
    else:
        return render(request, '403.html')  # Redirect if unauthorized

@login_required
def customer_dashboard(request):
    if request.user.groups.filter(name='Customer').exists():
        return render(request, 'customer_dashboard.html')
    else:
        return render(request, '403.html')  # Redirect if unauthorized