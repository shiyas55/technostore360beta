from django.db import models
from django.conf import settings
from products.models import Product

class Coupon(models.Model):
    DISCOUNT_TYPES = (
        ('percentage', 'Percentage Discount (%)'),
        ('fixed', 'Fixed Amount Discount ($)'),
    )

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, default='percentage')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(blank=True, null=True, help_text="Total overall times this coupon can be used")
    used_count = models.PositiveIntegerField(default=0)
    per_customer_limit = models.PositiveIntegerField(default=1, help_text="Usage limit per single customer")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.get_discount_type_display()} - {self.value})"

class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
        ('refunded', 'Refunded'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('bank_transfer', 'Bank Wire Transfer'),
        ('online', 'Online Payment Gateway'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refund_pending', 'Refund Pending'),
        ('refunded', 'Refunded'),
    )

    order_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='orders')
    
    # Statuses
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Financial breakdown
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Customer Info
    billing_address = models.JSONField(help_text="Snapshot of billing address parameters")
    shipping_address = models.JSONField(help_text="Snapshot of shipping address parameters")
    
    # Meta
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    customer_notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number} - {self.get_order_status_display()}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Purchase unit price")
    plan = models.CharField(max_length=20, default='monthly')

    @property
    def item_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Deleted Product'} in Order {self.order.order_number}"
