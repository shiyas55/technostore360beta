from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from decimal import Decimal
import random

from products.models import Product
from accounts.models import Address
from cart.cart import Cart
from .models import Order, OrderItem, Coupon

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your procurement cart is empty.")
        return redirect('cart_detail')

    # Verify stock of all products in cart
    for item in cart:
        product = item['product']
        qty = item['quantity']
        if product.stock_qty < qty:
            messages.error(request, f"Requested quantity ({qty}) for {product.name} exceeds available stock ({product.stock_qty}). Please adjust your cart.")
            return redirect('cart_detail')

    # Get user addresses
    addresses = Address.objects.filter(user=request.user)
    shipping_addresses = addresses.filter(address_type='shipping')
    billing_addresses = addresses.filter(address_type='billing')

    # Check for applied coupon
    coupon_code = request.session.get('coupon_code')
    coupon = None
    discount_amount = Decimal('0.00')
    subtotal = cart.get_subtotal()
    
    if coupon_code:
        coupon = Coupon.objects.filter(code__iexact=coupon_code, is_active=True).first()
        if coupon and coupon.start_date <= timezone.now() <= coupon.end_date and subtotal >= coupon.min_purchase:
            if coupon.discount_type == 'percentage':
                discount_amount = subtotal * (coupon.value / Decimal('100.00'))
                if coupon.max_discount and discount_amount > coupon.max_discount:
                    discount_amount = coupon.max_discount
            else: # fixed
                discount_amount = coupon.value
        else:
            # Clean expired / invalid coupon from session
            request.session['coupon_code'] = None
            request.session.modified = True

    # Recalculate totals
    tax_amount = cart.get_tax()
    shipping_cost = cart.get_shipping_cost()
    grand_total = subtotal - discount_amount + tax_amount + shipping_cost
    if grand_total < 0:
        grand_total = Decimal('0.00')

    if request.method == 'POST':
        shipping_addr_id = request.POST.get('shipping_address')
        billing_addr_id = request.POST.get('billing_address')
        payment_method = request.POST.get('payment_method', 'cod')
        customer_notes = request.POST.get('customer_notes', '')

        if not shipping_addr_id or not billing_addr_id:
            messages.error(request, "Please select both shipping and billing addresses.")
            return render(request, 'orders/checkout.html', {
                'cart': cart,
                'shipping_addresses': shipping_addresses,
                'billing_addresses': billing_addresses,
                'subtotal': subtotal,
                'discount': discount_amount,
                'tax': tax_amount,
                'shipping': shipping_cost,
                'total': grand_total,
                'coupon': coupon
            })

        shipping_address = get_object_or_404(Address, id=shipping_addr_id, user=request.user)
        billing_address = get_object_or_404(Address, id=billing_addr_id, user=request.user)

        # Build address snapshots as JSON
        shipping_snapshot = {
            'full_name': shipping_address.full_name,
            'phone': shipping_address.phone,
            'address_line1': shipping_address.address_line1,
            'address_line2': shipping_address.address_line2,
            'city': shipping_address.city,
            'district': shipping_address.district,
            'state': shipping_address.state,
            'country': shipping_address.country,
            'postal_code': shipping_address.postal_code,
        }

        billing_snapshot = {
            'full_name': billing_address.full_name,
            'phone': billing_address.phone,
            'address_line1': billing_address.address_line1,
            'address_line2': billing_address.address_line2,
            'city': billing_address.city,
            'district': billing_address.district,
            'state': billing_address.state,
            'country': billing_address.country,
            'postal_code': billing_address.postal_code,
        }

        # Generate unique order number
        order_number = f"T360-{timezone.now().strftime('%Y%m%d')}-{random.randint(100000, 999999)}"

        # Create order
        order = Order.objects.create(
            order_number=order_number,
            user=request.user,
            payment_method=payment_method,
            payment_status='paid' if payment_method == 'online' else 'pending',
            subtotal=subtotal,
            discount=discount_amount,
            tax=tax_amount,
            shipping_cost=shipping_cost,
            total=grand_total,
            shipping_address=shipping_snapshot,
            billing_address=billing_snapshot,
            customer_notes=customer_notes
        )

        # Create Order Items and decrease stock
        for item in cart:
            product = item['product']
            qty = item['quantity']
            price = item['price']
            plan = item.get('plan', 'monthly')
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                price=price,
                plan=plan
            )

            # Reduce product stock
            product.stock_qty -= qty
            product.save()

        # Update Coupon usage count
        if coupon:
            coupon.used_count += 1
            coupon.save()

        # Clear session cart and coupon
        cart.clear()
        if 'coupon_code' in request.session:
            del request.session['coupon_code']
        request.session.modified = True

        messages.success(request, f"Thank you! Your order {order_number} has been created successfully.")
        return redirect('order_confirmation', order_number=order_number)

    context = {
        'cart': cart,
        'shipping_addresses': shipping_addresses,
        'billing_addresses': billing_addresses,
        'subtotal': subtotal,
        'discount': discount_amount,
        'tax': tax_amount,
        'shipping': shipping_cost,
        'total': grand_total,
        'coupon': coupon
    }
    return render(request, 'orders/checkout.html', context)

@login_required
@require_POST
def coupon_apply(request):
    code = request.POST.get('coupon_code', '').strip()
    cart = Cart(request)
    subtotal = cart.get_subtotal()

    coupon = Coupon.objects.filter(code__iexact=code, is_active=True).first()
    
    if not coupon:
        return JsonResponse({'success': False, 'message': 'Invalid coupon code.'})
        
    if coupon.start_date > timezone.now() or coupon.end_date < timezone.now():
        return JsonResponse({'success': False, 'message': 'This coupon has expired.'})

    if subtotal < coupon.min_purchase:
        return JsonResponse({'success': False, 'message': f'Minimum purchase of INR {coupon.min_purchase} is required to use this coupon.'})

    if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
        return JsonResponse({'success': False, 'message': 'This coupon usage limit has been reached.'})

    # Save to session
    request.session['coupon_code'] = coupon.code
    request.session.modified = True
    
    # Calculate discount preview
    discount_amount = Decimal('0.00')
    if coupon.discount_type == 'percentage':
        discount_amount = subtotal * (coupon.value / Decimal('100.00'))
        if coupon.max_discount and discount_amount > coupon.max_discount:
            discount_amount = coupon.max_discount
    else:
        discount_amount = coupon.value

    return JsonResponse({
        'success': True,
        'message': f'Coupon "{coupon.code}" applied successfully!',
        'discount': float(discount_amount),
        'grand_total': float(subtotal - discount_amount + cart.get_tax() + cart.get_shipping_cost())
    })

@login_required
def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})

@login_required
def order_detail(request, order_number):
    # Allow order owner OR staff/manager to view order detail
    if request.user.is_staff or request.user.is_product_manager or request.user.is_order_manager or request.user.is_sales_manager:
        order = get_object_or_404(Order, order_number=order_number)
    else:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})

@login_required
def order_invoice(request, order_number):
    if request.user.is_staff or request.user.is_product_manager or request.user.is_order_manager or request.user.is_sales_manager:
        order = get_object_or_404(Order, order_number=order_number)
    else:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/invoice.html', {'order': order})

@login_required
def order_cancel(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    if order.order_status in ['pending', 'confirmed']:
        order.order_status = 'cancelled'
        order.save()
        
        # Restore stock for each item
        for item in order.items.all():
            if item.product:
                item.product.stock_qty += item.quantity
                item.product.save()
                
        messages.success(request, f"Order {order_number} has been cancelled and stock returned.")
    else:
        messages.error(request, "This order cannot be cancelled as it is already being processed or shipped.")
        
    return redirect('customer_dashboard')
