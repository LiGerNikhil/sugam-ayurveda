from django.urls import path
from . import views
from . import admin_views
from . import auth_views
from . import order_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('shipping-policy/', views.shipping_policy, name='shipping_policy'),
    path('return-policy/', views.return_policy, name='return_policy'),
    
    # User Authentication
    path('login/', auth_views.user_login, name='login'),
    path('register/', auth_views.user_register, name='register'),
    path('verify-email/<str:uidb64>/<str:token>/', auth_views.verify_email, name='verify_email'),
    path('verification-sent/', auth_views.verification_sent, name='verification_sent'),
    path('dashboard/', auth_views.user_dashboard, name='dashboard'),
    path('profile/', auth_views.user_profile, name='user_profile'),
    path('logout/', auth_views.user_logout, name='logout'),
    
    # Shopping Cart & Orders
    path('cart/', order_views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', order_views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', order_views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', order_views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', order_views.checkout, name='checkout'),
    path('order/<int:order_id>/confirmation/', order_views.order_confirmation, name='order_confirmation'),
    path('order/<int:order_id>/tracking/', order_views.order_tracking, name='order_tracking'),
    path('orders/', order_views.order_history, name='order_history'),
    path('payment-success/', order_views.payment_success, name='payment_success'),
    path('api/cart-count/', order_views.cart_count, name='cart_count'),
    path('api/create-razorpay-order/', order_views.create_razorpay_order, name='create_razorpay_order'),
    
    # Admin Dashboard URLs (separate from Django admin)
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/products/', admin_views.admin_products, name='admin_products'),
    path('admin-dashboard/products/add/', admin_views.admin_add_product, name='admin_add_product'),
    path('admin-dashboard/products/edit/<int:product_id>/', admin_views.admin_edit_product, name='admin_edit_product'),
    path('admin-dashboard/categories/', admin_views.admin_categories, name='admin_categories'),
    path('admin-dashboard/categories/add/', admin_views.admin_add_category, name='admin_add_category'),
    path('admin-dashboard/categories/edit/<str:category_id>/', admin_views.admin_edit_category, name='admin_edit_category'),
    path('admin-dashboard/categories/delete/<str:category_id>/', admin_views.admin_delete_category, name='admin_delete_category'),
    path('admin-dashboard/users/', admin_views.admin_users, name='admin_users'),
    path('admin-dashboard/orders/', admin_views.admin_orders, name='admin_orders'),
    path('admin-dashboard/site-info/', admin_views.admin_site_info, name='admin_site_info'),
    path('admin-dashboard/stats/', admin_views.admin_stats, name='admin_stats'),
    path('admin-dashboard/toggle-product-availability/<int:product_id>/', admin_views.toggle_product_availability, name='toggle_product_availability'),
    path('admin-dashboard/toggle-user-status/<int:user_id>/', admin_views.toggle_user_status, name='toggle_user_status'),
    path('admin-dashboard/update-order-status/<int:order_id>/', admin_views.update_order_status, name='update_order_status'),
]
