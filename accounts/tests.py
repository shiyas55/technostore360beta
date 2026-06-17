from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Address, Profile

User = get_user_model()

class AccountsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='corporate_buyer',
            email='buyer@corporate.com',
            password='testpassword123',
            first_name='John',
            last_name='Doe',
            is_customer=True
        )
        self.user.profile.company_name = "Buyer Corp"
        self.user.profile.phone_number = "1234567890"
        self.user.profile.save()

    def test_user_creation_and_profile(self):
        self.assertEqual(self.user.username, 'corporate_buyer')
        self.assertEqual(self.user.email, 'buyer@corporate.com')
        self.assertTrue(self.user.is_customer)
        self.assertEqual(self.user.profile.company_name, "Buyer Corp")
        self.assertEqual(str(self.user.profile), "corporate_buyer's Profile")

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post_success(self):
        # Test username login
        response = self.client.post(reverse('login'), {
            'username': 'corporate_buyer',
            'password': 'testpassword123'
        })
        self.assertRedirects(response, reverse('customer_dashboard'))

        # Logout and test email login
        self.client.logout()
        response = self.client.post(reverse('login'), {
            'username': 'buyer@corporate.com',
            'password': 'testpassword123'
        })
        self.assertRedirects(response, reverse('customer_dashboard'))

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': 'corporate_buyer',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200) # Re-renders page
        # Check that we stay on the login page and show error (messages framework)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn("Invalid corporate email/username or password.", str(messages[0]))

    def test_register_view_post_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'new_buyer',
            'email': 'new@corp.com',
            'password': 'newpassword123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'company_name': 'New Company Ltd',
            'phone_number': '0987654321'
        })
        self.assertRedirects(response, reverse('customer_dashboard'))
        self.assertTrue(User.objects.filter(username='new_buyer').exists())
        new_user = User.objects.get(username='new_buyer')
        self.assertEqual(new_user.profile.company_name, 'New Company Ltd')

    def test_register_view_post_existing_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'corporate_buyer',
            'email': 'different@corp.com',
            'password': 'newpassword123'
        })
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertIn("Username is already registered.", str(messages[0]))

    def test_customer_dashboard_unauthenticated(self):
        response = self.client.get(reverse('customer_dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('customer_dashboard')}")

    def test_customer_dashboard_authenticated(self):
        self.client.login(username='corporate_buyer', password='testpassword123')
        response = self.client.get(reverse('customer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')

    def test_profile_edit(self):
        self.client.login(username='corporate_buyer', password='testpassword123')
        response = self.client.post(reverse('profile_edit'), {
            'first_name': 'Johnny',
            'last_name': 'Does',
            'email': 'johnny@corporate.com',
            'company_name': 'Buyer Corporation',
            'phone_number': '1112223333'
        })
        self.assertRedirects(response, reverse('customer_dashboard'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Johnny')
        self.assertEqual(self.user.profile.company_name, 'Buyer Corporation')

    def test_address_crud(self):
        self.client.login(username='corporate_buyer', password='testpassword123')
        
        # Create address
        response = self.client.post(reverse('address_add'), {
            'full_name': 'John Doe Shipping',
            'phone': '1234567890',
            'address_line1': '123 Business Rd',
            'city': 'Bangalore',
            'state': 'Karnataka',
            'postal_code': '560001',
            'address_type': 'shipping',
            'is_default': 'true'
        })
        self.assertRedirects(response, reverse('customer_dashboard'))
        self.assertEqual(Address.objects.filter(user=self.user).count(), 1)
        address = Address.objects.get(user=self.user)
        self.assertTrue(address.is_default)

        # Edit address
        response = self.client.post(reverse('address_edit', args=[address.id]), {
            'full_name': 'John Doe Updated',
            'phone': '1234567890',
            'address_line1': '456 Commercial St',
            'city': 'Bangalore',
            'state': 'Karnataka',
            'postal_code': '560001',
            'address_type': 'shipping',
            'is_default': 'true'
        })
        self.assertRedirects(response, reverse('customer_dashboard'))
        address.refresh_from_db()
        self.assertEqual(address.full_name, 'John Doe Updated')
        self.assertEqual(address.address_line1, '456 Commercial St')

        # Delete address
        response = self.client.get(reverse('address_delete', args=[address.id]))
        self.assertRedirects(response, reverse('customer_dashboard'))
        self.assertEqual(Address.objects.filter(user=self.user).count(), 0)
