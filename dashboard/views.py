from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from django.http import HttpResponse
from django.utils import timezone
import csv
from decimal import Decimal

from products.models import Product, Category, Brand, Review
from orders.models import Order, OrderItem, Coupon

User = get_user_model()

# Helper decorator/checks for manager access
def is_manager(user):
    return user.is_authenticated and (
        user.is_staff or 
        user.is_product_manager or 
        user.is_order_manager or 
        user.is_sales_manager
    )

def manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        if is_manager(request.user):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Manager or Admin credentials required.")
        return redirect('home')
    return wrapper

def admin_login(request):
    if request.user.is_authenticated and is_manager(request.user):
        return redirect('admin_home')
        
    if request.method == 'POST':
        login_id = request.POST.get('username')
        password = request.POST.get('password')
        
        username = login_id
        if '@' in login_id:
            user_obj = User.objects.filter(email=login_id).first()
            if user_obj:
                username = user_obj.username
                
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if is_manager(user):
                login(request, user)
                messages.success(request, "Welcome to the Admin & Vendor Desk.")
                return redirect('admin_home')
            else:
                messages.error(request, "Access denied. You do not have manager privileges.")
        else:
            messages.error(request, "Invalid administrator credentials.")
            
    return render(request, 'dashboard/login.html')

@manager_required
def admin_home(request):
    # Total revenue from paid or delivered orders
    total_sales = Order.objects.filter(payment_status='paid').aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    
    # Order statistics
    total_orders_count = Order.objects.count()
    pending_orders_count = Order.objects.filter(order_status='pending').count()
    processing_orders_count = Order.objects.filter(order_status='processing').count()
    shipped_orders_count = Order.objects.filter(order_status='shipped').count()
    delivered_orders_count = Order.objects.filter(order_status='delivered').count()
    
    # Stock Alerts
    low_stock_products = Product.objects.filter(is_active=True, stock_qty__lte=5)
    
    # Active customers
    customers_count = User.objects.filter(is_customer=True, is_active=True).count()
    
    # Pending reviews
    pending_reviews_count = Review.objects.filter(is_approved=False).count()
    
    # Recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:5]

    context = {
        'total_sales': total_sales,
        'total_orders_count': total_orders_count,
        'pending_orders_count': pending_orders_count,
        'processing_orders_count': processing_orders_count,
        'shipped_orders_count': shipped_orders_count,
        'delivered_orders_count': delivered_orders_count,
        'low_stock_products': low_stock_products,
        'customers_count': customers_count,
        'pending_reviews_count': pending_reviews_count,
        'recent_orders': recent_orders
    }
    return render(request, 'dashboard/home.html', context)

@manager_required
def admin_products(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'dashboard/product_list.html', {'products': products})

@manager_required
def admin_product_add(request):
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        sku = request.POST.get('sku')
        category_id = request.POST.get('category')
        brand_id = request.POST.get('brand')
        short_desc = request.POST.get('short_desc')
        full_desc = request.POST.get('full_desc')
        price = request.POST.get('price', 0.00)
        sale_price = request.POST.get('sale_price')
        stock_qty = request.POST.get('stock_qty', 0)
        deployment = request.POST.get('deployment', 'Cloud / SaaS')
        business_type = request.POST.get('business_type', 'Enterprise & Mid-Market')
        support = request.POST.get('support', '24/7 Live Support')
        
        is_featured = request.POST.get('is_featured') == 'on' or request.POST.get('is_featured') == 'true'
        is_trending = request.POST.get('is_trending') == 'on' or request.POST.get('is_trending') == 'true'
        is_new_arrival = request.POST.get('is_new_arrival') == 'on' or request.POST.get('is_new_arrival') == 'true'
        is_best_seller = request.POST.get('is_best_seller') == 'on' or request.POST.get('is_best_seller') == 'true'
        
        category = get_object_or_404(Category, id=category_id)
        brand = get_object_or_404(Brand, id=brand_id)
        
        image_file = request.FILES.get('image_file')
        image_url = request.POST.get('image_url')

        product = Product.objects.create(
            name=name,
            sku=sku,
            category=category,
            brand=brand,
            short_desc=short_desc,
            full_desc=full_desc,
            price=price,
            sale_price=sale_price if sale_price else None,
            stock_qty=stock_qty,
            deployment=deployment,
            business_type=business_type,
            support=support,
            is_featured=is_featured,
            is_trending=is_trending,
            is_new_arrival=is_new_arrival,
            is_best_seller=is_best_seller,
            image_file=image_file,
            image=image_url if not image_file else None
        )
        
        messages.success(request, f"Product {product.name} created successfully.")
        return redirect('admin_products')

    return render(request, 'dashboard/product_form.html', {
        'categories': categories,
        'brands': brands,
        'action': 'Add'
    })

@manager_required
def admin_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.sku = request.POST.get('sku')
        product.category = get_object_or_404(Category, id=request.POST.get('category'))
        product.brand = get_object_or_404(Brand, id=request.POST.get('brand'))
        product.short_desc = request.POST.get('short_desc')
        product.full_desc = request.POST.get('full_desc')
        product.price = request.POST.get('price', 0.00)
        
        sale_price = request.POST.get('sale_price')
        product.sale_price = sale_price if sale_price else None
        
        product.stock_qty = request.POST.get('stock_qty', 0)
        product.deployment = request.POST.get('deployment', 'Cloud / SaaS')
        product.business_type = request.POST.get('business_type', 'Enterprise & Mid-Market')
        product.support = request.POST.get('support', '24/7 Live Support')
        
        product.is_featured = request.POST.get('is_featured') == 'on' or request.POST.get('is_featured') == 'true'
        product.is_trending = request.POST.get('is_trending') == 'on' or request.POST.get('is_trending') == 'true'
        product.is_new_arrival = request.POST.get('is_new_arrival') == 'on' or request.POST.get('is_new_arrival') == 'true'
        product.is_best_seller = request.POST.get('is_best_seller') == 'on' or request.POST.get('is_best_seller') == 'true'
        
        if request.FILES.get('image_file'):
            product.image_file = request.FILES.get('image_file')
            product.image = None
        elif request.POST.get('image_url'):
            product.image = request.POST.get('image_url')
            product.image_file = None
            
        product.save()
        messages.success(request, f"Product {product.name} updated successfully.")
        return redirect('admin_products')

    return render(request, 'dashboard/product_form.html', {
        'product': product,
        'categories': categories,
        'brands': brands,
        'action': 'Edit'
    })

@manager_required
def admin_product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    name = product.name
    product.delete()
    messages.success(request, f"Product {name} deleted successfully.")
    return redirect('admin_products')

@manager_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/order_list.html', {'orders': orders})

@manager_required
def admin_order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'dashboard/order_detail.html', {'order': order})

@manager_required
def admin_order_status_update(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if request.method == 'POST':
        status = request.POST.get('status')
        tracking = request.POST.get('tracking_number')
        notes = request.POST.get('admin_notes')
        
        if status in dict(Order.ORDER_STATUS_CHOICES):
            order.order_status = status
            
        if tracking is not None:
            order.tracking_number = tracking
            
        if notes is not None:
            order.admin_notes = notes
            
        order.save()
        messages.success(request, f"Order status updated to {order.get_order_status_display()}.")
    return redirect('admin_order_detail', order_number=order.order_number)

@manager_required
def admin_order_payment_update(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if request.method == 'POST':
        payment_status = request.POST.get('payment_status')
        if payment_status in dict(Order.PAYMENT_STATUS_CHOICES):
            order.payment_status = payment_status
            order.save()
            messages.success(request, f"Order payment status updated to {order.get_payment_status_display()}.")
    return redirect('admin_order_detail', order_number=order.order_number)

@manager_required
def admin_sales_report(request):
    # Overall summary metrics
    total_sales = Order.objects.filter(payment_status='paid').aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    total_orders = Order.objects.count()
    paid_orders = Order.objects.filter(payment_status='paid')
    
    # Calculate average order value
    avg_order_value = paid_orders.aggregate(avg=Avg('total'))['avg'] or Decimal('0.00')
    
    # Items sales summaries (Top selling products)
    top_selling_items = OrderItem.objects.values('product__name', 'product__sku')\
        .annotate(total_qty=Sum('quantity'), total_rev=Sum('price')*Sum('quantity'))\
        .order_by('-total_qty')[:10]

    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'top_selling_items': top_selling_items
    }
    return render(request, 'dashboard/sales_reports.html', context)

@manager_required
def admin_export_sales_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="sales_report_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Order Number', 'Date', 'Customer', 'Payment Method', 'Payment Status', 'Status', 'Subtotal (INR)', 'Discount (INR)', 'Tax (INR)', 'Total (INR)'])
    
    orders = Order.objects.all().order_by('-created_at')
    for o in orders:
        writer.writerow([
            o.order_number,
            o.created_at.strftime('%Y-%m-%d %H:%M'),
            o.user.email if o.user else 'Guest/Deleted',
            o.get_payment_method_display(),
            o.get_payment_status_display(),
            o.get_order_status_display(),
            o.subtotal,
            o.discount,
            o.tax,
            o.total
        ])
        
    return response

@manager_required
def admin_customers(request):
    customers = User.objects.filter(is_customer=True).order_by('-date_joined')
    return render(request, 'dashboard/customer_list.html', {'customers': customers})

@manager_required
def admin_customer_status_toggle(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Prevent locking out yourself
    if user == request.user:
        messages.error(request, "You cannot de-authorize your own administrator account.")
    else:
        user.is_active = not user.is_active
        user.save()
        status = "authorized" if user.is_active else "de-authorized / blocked"
        messages.success(request, f"Customer account {user.username} has been {status}.")
    return redirect('admin_customers')

@manager_required
def admin_reviews(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'dashboard/review_list.html', {'reviews': reviews})

@manager_required
def admin_review_approve(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.is_approved = True
    review.save()
    messages.success(request, f"Review by {review.user.username} has been approved.")
    return redirect('admin_reviews')

@manager_required
def admin_review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    messages.success(request, "Review deleted successfully.")
    return redirect('admin_reviews')

@manager_required
def admin_coupons(request):
    coupons = Coupon.objects.all().order_by('-start_date')
    return render(request, 'dashboard/coupon_list.html', {'coupons': coupons})

@manager_required
def admin_coupon_add(request):
    if request.method == 'POST':
        code = request.POST.get('code').strip().upper()
        discount_type = request.POST.get('discount_type', 'percentage')
        value = request.POST.get('value', 0.00)
        min_purchase = request.POST.get('min_purchase', 0.00)
        max_discount = request.POST.get('max_discount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        usage_limit = request.POST.get('usage_limit')
        is_active = request.POST.get('is_active') == 'on' or request.POST.get('is_active') == 'true'

        Coupon.objects.create(
            code=code,
            discount_type=discount_type,
            value=value,
            min_purchase=min_purchase,
            max_discount=max_discount if max_discount else None,
            start_date=start_date,
            end_date=end_date,
            usage_limit=usage_limit if usage_limit else None,
            is_active=is_active
        )
        messages.success(request, f"Coupon code {code} has been created.")
        return redirect('admin_coupons')
        
    return render(request, 'dashboard/coupon_form.html')
