from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import datetime

from products.models import Category, Brand, Product, Review
from orders.models import Order, Coupon

User = get_user_model()

class DashboardTestCase(TestCase):
    def setUp(self):
        # Create a product manager user
        self.mgr = User.objects.create_user(
            username='prod_mgr',
            email='pm@corporate.com',
            password='testpassword123',
            is_customer=False,
            is_product_manager=True
        )
        
        # Create a customer
        self.customer = User.objects.create_user(
            username='buyer',
            email='buyer@corporate.com',
            password='testpassword123',
            is_customer=True
        )

        self.category = Category.objects.create(name='Cloud Software', slug='cloud-software')
        self.brand = Brand.objects.create(name='Acme Corp', slug='acme-corp')
        
        self.product = Product.objects.create(
            name='Acme Cloud Storage',
            slug='acme-cloud-storage',
            sku='ACME-CS-001',
            category=self.category,
            brand=self.brand,
            price=20.00,
            stock_qty=10,
            deployment='Cloud / SaaS'
        )

        # Create a test order
        self.order = Order.objects.create(
            order_number='T360-TEST-123',
            user=self.customer,
            payment_method='cod',
            payment_status='pending',
            subtotal=1650.00,
            tax=297.00,
            shipping_cost=0.00,
            total=1947.00,
            shipping_address={'full_name': 'Test User'},
            billing_address={'full_name': 'Test User'}
        )

    def test_unauthenticated_manager_redirect(self):
        response = self.client.get(reverse('admin_home'))
        self.assertRedirects(response, reverse('admin_login'))

    def test_non_manager_access_denied(self):
        self.client.login(username='buyer', password='testpassword123')
        response = self.client.get(reverse('admin_home'))
        self.assertRedirects(response, reverse('home'))

    def test_manager_login_success(self):
        response = self.client.post(reverse('admin_login'), {
            'username': 'prod_mgr',
            'password': 'testpassword123'
        })
        self.assertRedirects(response, reverse('admin_home'))

    def test_admin_home_metrics(self):
        self.client.login(username='prod_mgr', password='testpassword123')
        response = self.client.get(reverse('admin_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/home.html')
        self.assertEqual(response.context['total_orders_count'], 1)
        self.assertEqual(response.context['customers_count'], 1)

    def test_product_crud_add(self):
        self.client.login(username='prod_mgr', password='testpassword123')
        
        # Add Product POST
        response = self.client.post(reverse('admin_product_add'), {
            'name': 'New Testing Product',
            'sku': 'NEW-SKU-999',
            'category': self.category.id,
            'brand': self.brand.id,
            'short_desc': 'Short desc',
            'full_desc': 'Full desc',
            'price': '99.99',
            'stock_qty': '50',
            'deployment': 'Hybrid',
            'business_type': 'Enterprise',
            'support': '24/7'
        })
        self.assertRedirects(response, reverse('admin_products'))
        self.assertTrue(Product.objects.filter(sku='NEW-SKU-999').exists())

    def test_product_crud_edit_delete(self):
        self.client.login(username='prod_mgr', password='testpassword123')
        
        # Edit Product
        response = self.client.post(reverse('admin_product_edit', args=[self.product.id]), {
            'name': 'Acme Updated Storage',
            'sku': 'ACME-CS-001',
            'category': self.category.id,
            'brand': self.brand.id,
            'price': '25.00',
            'stock_qty': '10'
        })
        self.assertRedirects(response, reverse('admin_products'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Acme Updated Storage')

        # Delete Product
        response = self.client.get(reverse('admin_product_delete', args=[self.product.id]))
        self.assertRedirects(response, reverse('admin_products'))
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_order_status_and_payment_updates(self):
        self.client.login(username='prod_mgr', password='testpassword123')
        
        # Update order status
        response = self.client.post(reverse('admin_order_status_update', args=[self.order.order_number]), {
            'status': 'processing',
            'tracking_number': 'TRK999888',
            'admin_notes': 'Processing notes'
        })
        self.assertRedirects(response, reverse('admin_order_detail', args=[self.order.order_number]))
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_status, 'processing')
        self.assertEqual(self.order.tracking_number, 'TRK999888')

        # Update order payment status
        response = self.client.post(reverse('admin_order_payment_update', args=[self.order.order_number]), {
            'payment_status': 'paid'
        })
        self.assertRedirects(response, reverse('admin_order_detail', args=[self.order.order_number]))
        self.order.refresh_from_db()
        self.assertEqual(self.order.payment_status, 'paid')

    def test_customer_blocking(self):
        self.client.login(username='prod_mgr', password='testpassword123')
        
        # De-authorize customer account
        response = self.client.get(reverse('admin_customer_status_toggle', args=[self.customer.id]))
        self.assertRedirects(response, reverse('admin_customers'))
        self.customer.refresh_from_db()
        self.assertFalse(self.customer.is_active)

        # Re-authorize customer account
        response = self.client.get(reverse('admin_customer_status_toggle', args=[self.customer.id]))
        self.assertRedirects(response, reverse('admin_customers'))
        self.customer.refresh_from_db()
        self.assertTrue(self.customer.is_active)

    def test_review_approval(self):
        review = Review.objects.create(
            product=self.product,
            user=self.customer,
            rating=4,
            comment='Decent storage',
            is_approved=False
        )
        self.client.login(username='prod_mgr', password='testpassword123')
        
        # Approve review
        response = self.client.get(reverse('admin_review_approve', args=[review.id]))
        self.assertRedirects(response, reverse('admin_reviews'))
        review.refresh_from_db()
        self.assertTrue(review.is_approved)

        # Delete review
        response = self.client.get(reverse('admin_review_delete', args=[review.id]))
        self.assertRedirects(response, reverse('admin_reviews'))
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_export_sales_csv(self):
        self.client.login(username='prod_mgr', password='testpassword123')
        response = self.client.get(reverse('admin_export_sales_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('T360-TEST-123', response.content.decode('utf-8'))

    def test_coupon_adding(self):
        self.client.login(username='prod_mgr', password='testpassword123')
        response = self.client.post(reverse('admin_coupon_add'), {
            'code': 'NEWYEAR50',
            'discount_type': 'percentage',
            'value': '50.00',
            'min_purchase': '2000.00',
            'max_discount': '1000.00',
            'start_date': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'end_date': (timezone.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': 'true'
        })
        self.assertRedirects(response, reverse('admin_coupons'))
        self.assertTrue(Coupon.objects.filter(code='NEWYEAR50').exists())
