from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import Profile, Address
from orders.models import Order

User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_product_manager or request.user.is_order_manager or request.user.is_sales_manager:
            return redirect('admin_home')
        return redirect('customer_dashboard')
        
    if request.method == 'POST':
        login_id = request.POST.get('username')
        password = request.POST.get('password')
        
        # B2B support: look up by email or username
        username = login_id
        if '@' in login_id:
            user_obj = User.objects.filter(email=login_id).first()
            if user_obj:
                username = user_obj.username
                
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if not user.is_active:
                messages.error(request, "Your account has been deactivated. Please contact support.")
                return render(request, 'accounts/login.html')
                
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            
            # Merge session guest cart if there is one
            guest_cart = request.session.get('cart', {})
            if guest_cart:
                from cart.cart import Cart
                cart = Cart(request)
                cart.merge_guest_cart(guest_cart)
                
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
                
            if user.is_staff or user.is_product_manager or user.is_order_manager or user.is_sales_manager:
                return redirect('admin_home')
            return redirect('customer_dashboard')
        else:
            messages.error(request, "Invalid corporate email/username or password.")
            
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('customer_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')
        phone_number = request.POST.get('phone_number')
        
        # Simple validations
        if not username or not email or not password:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'accounts/register.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already registered.")
            return render(request, 'accounts/register.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, "Corporate email is already registered.")
            return render(request, 'accounts/register.html')
            
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_customer=True
            )
            # Update Profile
            profile = user.profile
            profile.company_name = company_name
            profile.phone_number = phone_number
            profile.save()
            
            # Log user in
            login(request, user)
            messages.success(request, "Registration successful! Welcome to your corporate dashboard.")
            return redirect('customer_dashboard')
        except IntegrityError:
            messages.error(request, "An error occurred. Please try again.")
            
    return render(request, 'accounts/register.html')

@login_required
def customer_dashboard(request):
    # Fetch orders and addresses
    user_orders = Order.objects.filter(user=request.user)
    addresses = Address.objects.filter(user=request.user)
    
    context = {
        'orders': user_orders,
        'addresses': addresses,
        'profile': request.user.profile
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        profile.company_name = request.POST.get('company_name', profile.company_name)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.save()
        
        messages.success(request, "Your profile has been updated successfully.")
    return redirect('customer_dashboard')

@login_required
def address_add(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        address_type = request.POST.get('address_type', 'shipping')
        is_default = request.POST.get('is_default') == 'true'
        
        if not full_name or not phone or not address_line1 or not city or not state or not postal_code:
            messages.error(request, "Please fill in all required address fields.")
        else:
            Address.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                address_line1=address_line1,
                address_line2=address_line2,
                city=city,
                district=district,
                state=state,
                postal_code=postal_code,
                address_type=address_type,
                is_default=is_default
            )
            messages.success(request, "New address added successfully.")
            
    # Redirect to checkout if that's where the user came from
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('customer_dashboard')

@login_required
def address_edit(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        address.full_name = request.POST.get('full_name', address.full_name)
        address.phone = request.POST.get('phone', address.phone)
        address.address_line1 = request.POST.get('address_line1', address.address_line1)
        address.address_line2 = request.POST.get('address_line2', address.address_line2)
        address.city = request.POST.get('city', address.city)
        address.district = request.POST.get('district', address.district)
        address.state = request.POST.get('state', address.state)
        address.postal_code = request.POST.get('postal_code', address.postal_code)
        address.address_type = request.POST.get('address_type', address.address_type)
        address.is_default = request.POST.get('is_default') == 'true' or request.POST.get('is_default') == 'on'
        
        address.save()
        messages.success(request, "Address updated successfully.")
        
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('customer_dashboard')

@login_required
def address_delete(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, "Address deleted successfully.")
    
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('customer_dashboard')
