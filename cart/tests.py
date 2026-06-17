from django.test import TestCase
from django.urls import reverse
from products.models import Category, Brand, Product

class CartTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Cloud Software', slug='cloud-software')
        self.brand = Brand.objects.create(name='Acme Corp', slug='acme-corp')
        self.product = Product.objects.create(
            name='Acme Cloud Storage',
            slug='acme-cloud-storage',
            sku='ACME-CS-001',
            category=self.category,
            brand=self.brand,
            price=29.99, # USD
            stock_qty=10,
            deployment='Cloud / SaaS'
        )

    def test_cart_operations(self):
        # Add to cart POST
        response = self.client.post(reverse('cart_add', args=[self.product.id]), {
            'quantity': '2'
        })
        self.assertRedirects(response, reverse('cart_detail'))
        
        # Verify cart content via session
        cart_data = self.client.session.get('cart')
        self.assertEqual(cart_data, {f"{self.product.id}_monthly": 2})

    def test_cart_add_exceeding_stock(self):
        # Add 12 items (max stock is 10)
        response = self.client.post(reverse('cart_add', args=[self.product.id]), {
            'quantity': '12'
        })
        self.assertRedirects(response, reverse('cart_detail'))
        
        cart_data = self.client.session.get('cart')
        self.assertEqual(cart_data, {f"{self.product.id}_monthly": 10}) # capped at stock_qty

        # Adding more items when already at max should display warning
        response = self.client.post(reverse('cart_add', args=[self.product.id]), {
            'quantity': '2'
        })
        self.assertRedirects(response, reverse('cart_detail'))
        messages = list(response.wsgi_request._messages)
        self.assertIn("already have the maximum available stock", str(messages[0]))

    def test_cart_ajax_update(self):
        # Add product first
        self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': '1'})
        
        # Update quantity via AJAX (cart_update view requires POST)
        response = self.client.post(reverse('cart_update', args=[self.product.id]), {
            'quantity': '5'
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['item_qty'], 5)
        self.assertEqual(json_data['cart_len'], 5)

        # Check session reflects new qty
        self.assertEqual(self.client.session.get('cart'), {f"{self.product.id}_monthly": 5})

    def test_cart_remove_and_clear(self):
        self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': '3'})
        
        # Remove product
        response = self.client.get(reverse('cart_remove', args=[self.product.id]))
        self.assertRedirects(response, reverse('cart_detail'))
        self.assertNotIn(f"{self.product.id}_monthly", self.client.session.get('cart', {}))

        # Re-add and clear
        self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': '2'})
        response = self.client.get(reverse('cart_clear'))
        self.assertRedirects(response, reverse('cart_detail'))
        self.assertEqual(self.client.session.get('cart'), {})
