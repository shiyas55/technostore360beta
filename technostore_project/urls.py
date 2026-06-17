from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Import views
from core import views as core_views
from accounts import views as accounts_views
from products import views as products_views
from cart import views as cart_views
from orders import views as orders_views
from dashboard import views as dashboard_views

urlpatterns = [
    # Built-in django admin (fallback)
    path('admin-console/', admin.site.urls),

    # App: core (landing pages)
    path('', core_views.home, name='home'),
    path('packages/', core_views.solution_packages, name='solution_packages'),
    path('compare/', core_views.product_compare, name='product_compare'),
    path('demo/', core_views.demo_request, name='demo_request'),
    path('vendors/', core_views.reseller_dashboard, name='reseller_dashboard'),

    # App: accounts (SSO / Profiles / Dashboard)
    path('accounts/login/', accounts_views.login_view, name='login'),
    path('accounts/logout/', accounts_views.logout_view, name='logout'),
    path('accounts/register/', accounts_views.register_view, name='register'),
    path('accounts/dashboard/', accounts_views.customer_dashboard, name='customer_dashboard'),
    path('accounts/profile/edit/', accounts_views.profile_edit, name='profile_edit'),
    path('accounts/address/add/', accounts_views.address_add, name='address_add'),
    path('accounts/address/edit/<int:address_id>/', accounts_views.address_edit, name='address_edit'),
    path('accounts/address/delete/<int:address_id>/', accounts_views.address_delete, name='address_delete'),

    # App: products (catalog & details)
    path('products/', products_views.product_list, name='product_list'),
    path('products/<slug:slug>/', products_views.product_detail, name='product_detail'),
    path('products/<slug:slug>/review/', products_views.submit_review, name='submit_review'),
    path('wishlist/add/<int:product_id>/', products_views.wishlist_add, name='wishlist_add'),
    path('wishlist/remove/<int:product_id>/', products_views.wishlist_remove, name='wishlist_remove'),

    # App: cart (session operations)
    path('cart/', cart_views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', cart_views.cart_add, name='cart_add'),
    path('cart/update/<int:product_id>/', cart_views.cart_update, name='cart_update'),
    path('cart/remove/<int:product_id>/', cart_views.cart_remove, name='cart_remove'),
    path('cart/clear/', cart_views.cart_clear, name='cart_clear'),

    # App: orders (checkout & invoices)
    path('checkout/', orders_views.checkout, name='checkout'),
    path('checkout/coupon/', orders_views.coupon_apply, name='coupon_apply'),
    path('checkout/confirmation/<str:order_number>/', orders_views.order_confirmation, name='order_confirmation'),
    path('order/detail/<str:order_number>/', orders_views.order_detail, name='order_detail'),
    path('order/invoice/<str:order_number>/', orders_views.order_invoice, name='order_invoice'),
    path('order/cancel/<str:order_number>/', orders_views.order_cancel, name='order_cancel'),

    # App: dashboard (Custom admin desk)
    path('dashboard/', dashboard_views.admin_home, name='admin_home'),
    path('dashboard/login/', dashboard_views.admin_login, name='admin_login'),
    path('dashboard/products/', dashboard_views.admin_products, name='admin_products'),
    path('dashboard/products/add/', dashboard_views.admin_product_add, name='admin_product_add'),
    path('dashboard/products/edit/<int:product_id>/', dashboard_views.admin_product_edit, name='admin_product_edit'),
    path('dashboard/products/delete/<int:product_id>/', dashboard_views.admin_product_delete, name='admin_product_delete'),
    path('dashboard/orders/', dashboard_views.admin_orders, name='admin_orders'),
    path('dashboard/orders/<str:order_number>/', dashboard_views.admin_order_detail, name='admin_order_detail'),
    path('dashboard/orders/<str:order_number>/status/', dashboard_views.admin_order_status_update, name='admin_order_status_update'),
    path('dashboard/orders/<str:order_number>/payment/', dashboard_views.admin_order_payment_update, name='admin_order_payment_update'),
    path('dashboard/sales/', dashboard_views.admin_sales_report, name='admin_sales_report'),
    path('dashboard/sales/export/', dashboard_views.admin_export_sales_csv, name='admin_export_sales_csv'),
    path('dashboard/customers/', dashboard_views.admin_customers, name='admin_customers'),
    path('dashboard/customers/<int:user_id>/status/', dashboard_views.admin_customer_status_toggle, name='admin_customer_status_toggle'),
    path('dashboard/reviews/', dashboard_views.admin_reviews, name='admin_reviews'),
    path('dashboard/reviews/<int:review_id>/approve/', dashboard_views.admin_review_approve, name='admin_review_approve'),
    path('dashboard/reviews/<int:review_id>/delete/', dashboard_views.admin_review_delete, name='admin_review_delete'),
    path('dashboard/coupons/', dashboard_views.admin_coupons, name='admin_coupons'),
    path('dashboard/coupons/add/', dashboard_views.admin_coupon_add, name='admin_coupon_add'),
]

# Media and Static files routing during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
