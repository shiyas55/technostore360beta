from django.test import TestCase
from django.urls import reverse
from products.models import Category, Brand, Product

class CoreTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Cloud Software', slug='cloud-software')
        self.brand = Brand.objects.create(name='Acme Corp', slug='acme-corp')
        self.product1 = Product.objects.create(
            name='Acme Storage A',
            slug='acme-storage-a',
            sku='ACME-CS-001',
            category=self.category,
            brand=self.brand,
            price=20.00,
            stock_qty=10
        )
        self.product2 = Product.objects.create(
            name='Acme Storage B',
            slug='acme-storage-b',
            sku='ACME-CS-002',
            category=self.category,
            brand=self.brand,
            price=30.00,
            stock_qty=10
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertContains(response, 'Acme Storage A')

    def test_packages_page(self):
        response = self.client.get(reverse('solution_packages'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/packages.html')
        self.assertContains(response, 'Startup Launch Kit')

    def test_compare_matrix(self):
        # 1. View comparison page (initially empty)
        response = self.client.get(reverse('product_compare'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/compare.html')

        # 2. Add product1 to compare list
        response = self.client.get(reverse('product_compare'), {'action': 'add', 'sku': 'ACME-CS-001'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session.get('compared_products'), ['ACME-CS-001'])

        # 3. Add product2 to compare list
        response = self.client.get(reverse('product_compare'), {'action': 'add', 'sku': 'ACME-CS-002'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session.get('compared_products'), ['ACME-CS-001', 'ACME-CS-002'])

        # 4. Remove product1 from compare list
        response = self.client.get(reverse('product_compare'), {'action': 'remove', 'sku': 'ACME-CS-001'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session.get('compared_products'), ['ACME-CS-002'])

        # 5. Clear compare list
        response = self.client.get(reverse('product_compare'), {'action': 'clear'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session.get('compared_products'), [])

    def test_demo_request(self):
        # View demo page with product SKU
        response = self.client.get(reverse('demo_request'), {'product': 'ACME-CS-001'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/demo.html')
        self.assertContains(response, 'Acme Storage A')

        # Submit demo request POST
        response = self.client.post(reverse('demo_request'), {
            'name': 'B2B Client',
            'email': 'client@b2b.com',
            'company': 'B2B Client Corp',
            'phone': '1234567890',
            'scale': '10-50',
            'interest': 'Cloud Software',
            'message': 'Looking for a custom solution.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/demo_success.html')
        self.assertContains(response, 'B2B Client Corp')

    def test_reseller_page(self):
        response = self.client.get(reverse('reseller_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/reseller.html')
