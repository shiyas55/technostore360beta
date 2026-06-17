from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False, plan='monthly'):
        item_key = f"{product.id}_{plan}"
        if item_key not in self.cart:
            self.cart[item_key] = 0
            
        if override_quantity:
            self.cart[item_key] = quantity
        else:
            self.cart[item_key] += quantity
            
        # Ensure quantity does not exceed stock
        if self.cart[item_key] > product.stock_qty:
            self.cart[item_key] = product.stock_qty
            
        if self.cart[item_key] <= 0:
            self.remove(product, plan)
            
        self.save()

    def remove(self, product, plan='monthly'):
        item_key = f"{product.id}_{plan}"
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_keys = self.cart.keys()
        product_ids = []
        for key in product_keys:
            if '_' in key:
                prod_id = key.split('_')[0]
            else:
                prod_id = key
            if prod_id not in product_ids:
                product_ids.append(prod_id)
                
        products = Product.objects.filter(id__in=product_ids)
        product_dict = {str(p.id): p for p in products}
        
        for item_key, quantity in list(self.cart.items()):
            if '_' in item_key:
                parts = item_key.split('_')
                product_id = parts[0]
                plan = parts[1]
            else:
                product_id = item_key
                plan = 'monthly'
                
            product = product_dict.get(product_id)
            if product:
                base_price = Decimal(product.current_price_in_inr)
                if plan == 'yearly':
                    # Yearly price is monthly price * 12, with a 10% B2B discount
                    price = base_price * Decimal('12') * Decimal('0.90')
                else:
                    price = base_price
                    
                item = {
                    'product': product,
                    'quantity': quantity,
                    'plan': plan,
                    'price': price,
                    'total_price': price * quantity
                }
                yield item

    def __len__(self):
        return sum(qty for qty in self.cart.values())

    def get_subtotal(self):
        subtotal = Decimal('0.00')
        for item in self:
            subtotal += item['total_price']
        return subtotal

    def get_tax(self):
        # 18% GST standard for tech products in India
        return self.get_subtotal() * Decimal('0.18')

    def get_shipping_cost(self):
        # Free shipping for B2B orders above 50,000 INR, else 1,500 INR B2B transit charge
        subtotal = self.get_subtotal()
        if subtotal == 0 or subtotal > 50000:
            return Decimal('0.00')
        return Decimal('1500.00')

    def get_total(self):
        return self.get_subtotal() + self.get_tax() + self.get_shipping_cost()

    def clear(self):
        del self.session['cart']
        self.save()

    def merge_guest_cart(self, guest_cart):
        """
        Merge items from guest cart into this cart (user-logged-in cart).
        """
        for item_key, qty in guest_cart.items():
            if item_key in self.cart:
                self.cart[item_key] += qty
            else:
                self.cart[item_key] = qty
        self.save()
