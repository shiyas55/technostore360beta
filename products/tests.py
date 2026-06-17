from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Brand, Product, Review, Wishlist
from orders.models import Order, OrderItem

User = get_user_model()

class ProductsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
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
            short_desc='B2B cloud storage solution',
            full_desc='Full description of Acme Cloud Storage',
            price=29.99,
            stock_qty=100,
            deployment='Cloud / SaaS'
        )

    def test_product_model_properties(self):
        self.assertEqual(self.product.current_price, 29.99)
        self.assertEqual(self.product.price_in_inr, 29.99 * 82.5)
        self.assertTrue(self.product.is_in_stock)
        self.assertEqual(self.product.stock_status, 'in_stock')
        self.assertEqual(self.product.average_rating, 5.0) # default fallback
        self.assertEqual(self.product.reviews_count, 0)

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/list.html')
        self.assertContains(response, 'Acme Cloud Storage')

    def test_product_list_filtering(self):
        # Category filter
        response = self.client.get(reverse('product_list'), {'category': 'cloud-software'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Acme Cloud Storage')

        # Empty category filter
        response = self.client.get(reverse('product_list'), {'category': 'other-category'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Acme Cloud Storage')

        # Price filter under-50
        response = self.client.get(reverse('product_list'), {'price': 'under-50'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Acme Cloud Storage')

        # Price filter over-50
        response = self.client.get(reverse('product_list'), {'price': 'over-50'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Acme Cloud Storage')

        # Deployment filter
        response = self.client.get(reverse('product_list'), {'deployment': ['Cloud / SaaS']})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Acme Cloud Storage')

        # Search query
        response = self.client.get(reverse('product_list'), {'search': 'Acme'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Acme Cloud Storage')

        response = self.client.get(reverse('product_list'), {'search': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Acme Cloud Storage')

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/detail.html')
        self.assertContains(response, 'Acme Cloud Storage')

    def test_submit_review(self):
        self.client.login(username='buyer', password='testpassword123')
        
        # Test standard review
        response = self.client.post(reverse('submit_review', args=[self.product.slug]), {
            'rating': '4',
            'comment': 'Good storage solution.'
        })
        self.assertRedirects(response, reverse('product_detail', args=[self.product.slug]))
        self.assertEqual(Review.objects.filter(product=self.product).count(), 1)
        review = Review.objects.get(product=self.product)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, 'Good storage solution.')
        self.assertFalse(review.is_verified_purchase)

        # Duplicate review should fail
        response = self.client.post(reverse('submit_review', args=[self.product.slug]), {
            'rating': '5',
            'comment': 'Another review.'
        })
        self.assertRedirects(response, reverse('product_detail', args=[self.product.slug]))
        self.assertEqual(Review.objects.filter(product=self.product).count(), 1)

    def test_wishlist_add_and_remove(self):
        self.client.login(username='buyer', password='testpassword123')
        
        # Add to wishlist
        response = self.client.get(reverse('wishlist_add', args=[self.product.id]))
        self.assertRedirects(response, reverse('product_detail', args=[self.product.slug]))
        self.assertTrue(Wishlist.objects.filter(user=self.user, product=self.product).exists())

        # Remove from wishlist
        response = self.client.get(reverse('wishlist_remove', args=[self.product.id]))
        self.assertRedirects(response, reverse('customer_dashboard'))
        self.assertFalse(Wishlist.objects.filter(user=self.user, product=self.product).exists())
