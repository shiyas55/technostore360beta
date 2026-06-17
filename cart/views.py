from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .cart import Cart

def cart_detail(request):
    return render(request, 'cart/cart.html')

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity_str = request.POST.get('quantity', 1)
    try:
        quantity = int(quantity_str)
    except ValueError:
        quantity = 1
        
    override_quantity_str = request.POST.get('override', 'false')
    override_quantity = override_quantity_str.lower() == 'true'
    plan = request.POST.get('plan', 'monthly')

    if product.stock_qty <= 0:
        messages.error(request, f"{product.name} is currently out of stock.")
        return redirect('product_detail', slug=product.slug)

    # Check if quantity requested is greater than stock
    available_stock = product.stock_qty
    item_key = f"{product.id}_{plan}"
    current_cart_qty = cart.cart.get(item_key, 0)
    
    if not override_quantity and (current_cart_qty + quantity > available_stock):
        quantity = available_stock - current_cart_qty
        if quantity > 0:
            messages.warning(request, f"Only {available_stock} items of {product.name} are available. Added remaining items to your cart.")
        else:
            messages.warning(request, f"You already have the maximum available stock ({available_stock}) of {product.name} in your cart.")
            return redirect('cart_detail')
            
    cart.add(product=product, quantity=quantity, override_quantity=override_quantity, plan=plan)
    messages.success(request, f"Added {product.name} ({plan.title()} Plan) to your procurement cart.")
    
    # Check if buy_now button was clicked
    if request.POST.get('buy_now') == 'true':
        return redirect('checkout')
        
    return redirect('cart_detail')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity_str = request.POST.get('quantity')
    plan = request.POST.get('plan', 'monthly')
    try:
        quantity = int(quantity_str)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid quantity'}, status=400)
        
    if quantity > product.stock_qty:
        quantity = product.stock_qty
        messages.warning(request, f"Requested quantity exceeds available stock. Adjusted to {product.stock_qty} (max).")
        
    cart.add(product=product, quantity=quantity, override_quantity=True, plan=plan)
    
    # Return JSON response for AJAX updates
    return JsonResponse({
        'success': True,
        'item_qty': quantity,
        'cart_len': len(cart),
        'subtotal': float(cart.get_subtotal()),
        'tax': float(cart.get_tax()),
        'shipping': float(cart.get_shipping_cost()),
        'total': float(cart.get_total())
    })

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    plan = request.GET.get('plan', 'monthly')
    cart.remove(product, plan=plan)
    messages.success(request, f"Removed {product.name} ({plan.title()} Plan) from your cart.")
    return redirect('cart_detail')

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, "Procurement cart cleared.")
    return redirect('cart_detail')
