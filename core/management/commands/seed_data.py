import os
import json
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from accounts.models import Profile, Address
from products.models import Category, Brand, Product, ProductFeature, ProductSpec, Review

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds database with categories, brands, products, and default accounts from data.js"

    def handle(self, *args, **options):
        self.stdout.write("Parsing data.js file using Node.js...")
        
        # Paths
        base_dir = settings.BASE_DIR
        data_js_path = os.path.join(base_dir, 'js', 'data.js')
        
        if not os.path.exists(data_js_path):
            self.stdout.write(self.style.ERROR(f"Could not find data.js at {data_js_path}"))
            return

        # Prepare Node script to output JSON representation of the constants
        node_script = f"""
const fs = require('fs');
let content = fs.readFileSync('{data_js_path}', 'utf8');
content += '\\nconsole.log(JSON.stringify({{categories, products, solutionPackages}}));';
fs.writeFileSync('temp_data.js', content);
"""
        
        try:
            # Create a temp JS file and execute it
            subprocess.run(['node', '-e', node_script], check=True)
            result = subprocess.run(['node', 'temp_data.js'], capture_output=True, text=True, check=True)
            # Remove temp file
            if os.path.exists('temp_data.js'):
                os.remove('temp_data.js')
                
            raw_data = json.loads(result.stdout)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to execute Node script: {e}"))
            if os.path.exists('temp_data.js'):
                os.remove('temp_data.js')
            return

        # 1. Create Default Users (Super Admin, Managers, Customer)
        self.stdout.write("Seeding accounts...")
        
        # Superuser / Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            email='admin@technostore360.com',
            defaults={
                'is_staff': True,
                'is_superuser': True,
                'is_customer': False
            }
        )
        if created:
            admin_user.set_password('admin')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Super Admin created: username='admin', password='admin'"))

        # Product Manager
        pm_user, created = User.objects.get_or_create(
            username='product_mgr',
            email='pm@technostore360.com',
            defaults={
                'is_staff': True,
                'is_product_manager': True,
                'is_customer': False
            }
        )
        if created:
            pm_user.set_password('pm123')
            pm_user.save()
            self.stdout.write(self.style.SUCCESS("Product Manager created: username='product_mgr', password='pm123'"))

        # Customer
        customer_user, created = User.objects.get_or_create(
            username='customer',
            email='shiyas@technostore360.com',
            defaults={
                'is_customer': True
            }
        )
        if created:
            customer_user.set_password('customer123')
            customer_user.save()
            
            # Setup profile details
            profile = customer_user.profile
            profile.company_name = "Global Tech Solutions"
            profile.phone_number = "+91 9876543210"
            profile.save()

            # Create default address
            Address.objects.get_or_create(
                user=customer_user,
                full_name="Shiyas Ahmad",
                phone="+91 96337 06212",
                address_line1="Kinfra Tech Park, Kakkanchery",
                address_line2="Block B, 2nd Floor",
                city="Kozhikode",
                district="Malappuram",
                state="Kerala",
                country="India",
                postal_code="673635",
                address_type='shipping',
                is_default=True
            )
            self.stdout.write(self.style.SUCCESS("Customer account created: username='customer', password='customer123'"))

        # 2. Seed Categories
        self.stdout.write("Seeding categories...")
        categories_map = {}
        for idx, cat_data in enumerate(raw_data.get('categories', [])):
            slug = cat_data.get('id')
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': cat_data.get('title'),
                    'description': cat_data.get('description', ''),
                    'icon': cat_data.get('icon', 'layers'),
                    'display_order': idx,
                    'is_active': True
                }
            )
            categories_map[slug] = category
            if created:
                self.stdout.write(f"Created Category: {category.name}")

        # 3. Seed Brands
        self.stdout.write("Seeding brands...")
        brands_map = {}
        products_data = raw_data.get('products', [])
        unique_brands = sorted(list(set(p.get('brand') for p in products_data if p.get('brand'))))
        
        for brand_name in unique_brands:
            slug = slugify(brand_name)
            brand, created = Brand.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': brand_name,
                    'is_active': True
                }
            )
            brands_map[brand_name] = brand
            if created:
                self.stdout.write(f"Created Brand: {brand.name}")

        # 4. Seed Products
        self.stdout.write("Seeding products...")
        for idx, prod_data in enumerate(products_data):
            name = prod_data.get('name')
            sku = prod_data.get('id')
            brand_name = prod_data.get('brand')
            cat_slug = prod_data.get('categoryId')
            
            category = categories_map.get(cat_slug) or list(categories_map.values())[0]
            brand = brands_map.get(brand_name) or list(brands_map.values())[0]
            
            # Map pricing (originalPrice is regular price, price is sale price)
            price_val = prod_data.get('originalPrice') or prod_data.get('price') or 0.00
            sale_price_val = prod_data.get('price') if prod_data.get('originalPrice') else None
            
            # Slugify name
            slug = slugify(name)
            
            # Ensure unique slug
            if Product.objects.filter(slug=slug).exists():
                slug = f"{slug}-{sku}"
                
            product, created = Product.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': name,
                    'slug': slug,
                    'category': category,
                    'brand': brand,
                    'short_desc': prod_data.get('shortDesc', ''),
                    'full_desc': prod_data.get('longDesc', ''),
                    'image': prod_data.get('imageUrl', ''),
                    'price': price_val,
                    'sale_price': sale_price_val,
                    'stock_qty': 99, # default stock to keep in stock
                    'is_active': True,
                    'is_featured': idx < 6,
                    'is_trending': 'dealHighlight' in prod_data,
                    'is_new_arrival': idx % 3 == 0,
                    'is_best_seller': prod_data.get('rating', 0.0) >= 4.5,
                    'deployment': prod_data.get('deployment', 'Cloud / SaaS'),
                    'business_type': prod_data.get('businessType', 'Enterprise & Mid-Market'),
                    'support': prod_data.get('support', '24/7 Live Support'),
                    'best_use_case': prod_data.get('bestUseCase', ''),
                    'demo_available': prod_data.get('demoAvailable', True)
                }
            )
            
            if created:
                # Add features
                for feat_text in prod_data.get('features', []):
                    ProductFeature.objects.create(product=product, feature=feat_text)
                
                # Add default specifications
                specs = [
                    ('Deployment', product.deployment),
                    ('Business Type', product.business_type),
                    ('Support', product.support),
                    ('Best Use Case', product.best_use_case),
                ]
                for s_name, s_val in specs:
                    if s_val:
                        ProductSpec.objects.create(product=product, name=s_name, value=s_val)

                # Add a sample review
                Review.objects.create(
                    product=product,
                    user=customer_user,
                    rating=int(float(prod_data.get('rating', 5.0))),
                    comment="Excellent product. The integration is seamless and the B2B features are highly reliable.",
                    is_approved=True,
                    is_verified_purchase=True
                )
                
                self.stdout.write(f"Created Product: {product.name} (SKU: {product.sku})")
                
        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
