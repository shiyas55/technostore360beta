from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import datetime

from products.models import Category, Brand, Product
from accounts.models import Address
from orders.models import Order, OrderItem, Coupon

User = get_user_model()

class OrdersTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='buyer',
            email='buyer@corporate.com',
            password='testpassword123',
            is_customer=True
        )
        self.client.login(username='buyer', password='testpassword123')

        self.category = Category.objects.create(name='Cloud Software', slug='cloud-software')
        self.brand = Brand.objects.create(name='Acme Corp', slug='acme-corp')
        self.product = Product.objects.create(
            name='Acme Cloud Storage',
            slug='acme-cloud-storage',
            sku='ACME-CS-001',
            category=self.category,
            brand=self.brand,
            price=20.00, # USD -> INR = 1650.00
            stock_qty=10,
            deployment='Cloud / SaaS'
        )

        self.shipping_address = Address.objects.create(
            user=self.user,
            full_name='John Shipping',
            phone='1234567890',
            address_line1='123 Shipping Rd',
            city='Bangalore',
            state='Karnataka',
            postal_code='560001',
            address_type='shipping',
            is_default=True
        )

        self.billing_address = Address.objects.create(
            user=self.user,
            full_name='John Billing',
            phone='1234567890',
            address_line1='456 Billing St',
            city='Bangalore',
            state='Karnataka',
            postal_code='560001',
            address_type='billing',
            is_default=True
        )

        self.coupon = Coupon.objects.create(
            code='DISCOUNT10',
            discount_type='percentage',
            value=Decimal('10.00'),
            min_purchase=Decimal('100.00'),
            start_date=timezone.now() - datetime.timedelta(days=1),
            end_date=timezone.now() + datetime.timedelta(days=2),
            is_active=True
        )

    def test_checkout_page_redirect_if_cart_empty(self):
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, reverse('cart_detail'))

    def test_coupon_apply_ajax_success(self):
        # Add to cart so subtotal > min_purchase
        self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': '1'})
        # Subtotal will be 1650.00 INR (> min_purchase of 100.00)
        
        response = self.client.post(reverse('coupon_apply'), {
            'coupon_code': 'DISCOUNT10'
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['discount'], 165.0) # 10% of 1650

    def test_coupon_apply_ajax_invalid(self):
        response = self.client.post(reverse('coupon_apply'), {
            'coupon_code': 'NONEXISTENT'
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertFalse(json_data['success'])

    def test_checkout_and_order_creation(self):
        # Add to cart
        self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': '2'})

        # Post checkout form
        response = self.client.post(reverse('checkout'), {
            'shipping_address': self.shipping_address.id,
            'billing_address': self.billing_address.id,
            'payment_method': 'bank_transfer',
            'customer_notes': 'Please deliver during office hours.'
        })
        
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertRedirects(response, reverse('order_confirmation', args=[order.order_number]))
        
        # Verify order details
        self.assertEqual(order.payment_method, 'bank_transfer')
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product, self.product)
        self.assertEqual(order.items.first().quantity, 2)
        
        # Verify stock decreased
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_qty, 8) # 10 - 2

        # Verify address snapshot
        self.assertEqual(order.shipping_address['full_name'], 'John Shipping')
        self.assertEqual(order.billing_address['full_name'], 'John Billing')

    def test_order_cancellation(self):
        # Create order
        self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': '2'})
        self.client.post(reverse('checkout'), {
            'shipping_address': self.shipping_address.id,
            'billing_address': self.billing_address.id,
            'payment_method': 'cod'
        })
        
        order = Order.objects.first()
        self.assertEqual(order.order_status, 'pending')

        # Cancel order
        response = self.client.get(reverse('order_cancel', args=[order.order_number]))
        self.assertRedirects(response, reverse('customer_dashboard'))
        
        order.refresh_from_db()
        self.assertEqual(order.order_status, 'cancelled')

        # Verify stock restored
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_qty, 10) # 8 + 2

    def test_invoice_and_detail_views(self):
        # Create order
        self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': '1'})
        self.client.post(reverse('checkout'), {
            'shipping_address': self.shipping_address.id,
            'billing_address': self.billing_address.id,
            'payment_method': 'cod'
        })
        order = Order.objects.first()

        # Check detail view
        response = self.client.get(reverse('order_detail', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/detail.html')

        # Check invoice view
        response = self.client.get(reverse('order_invoice', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/invoice.html')

    def test_yearly_plan_checkout(self):
        # Add to cart with yearly plan
        self.client.post(reverse('cart_add', args=[self.product.id]), {
            'quantity': '1',
            'plan': 'yearly'
        })
        
        # Checkout
        response = self.client.post(reverse('checkout'), {
            'shipping_address': self.shipping_address.id,
            'billing_address': self.billing_address.id,
            'payment_method': 'cod'
        })
        
        # Verify order contains yearly plan
        order = Order.objects.first()
        self.assertEqual(order.items.count(), 1)
        order_item = order.items.first()
        self.assertEqual(order_item.plan, 'yearly')
        
        # Verify yearly discount pricing: 20 * 82.5 * 12 * 0.9 = 17820.0
        self.assertEqual(float(order_item.price), 17820.0)
