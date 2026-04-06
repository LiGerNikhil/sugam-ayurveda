from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    id = models.SlugField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    PRODUCT_TYPES = [
        ('single', 'Single'),
        ('bundle', 'Bundle'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sub_category = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    size = models.CharField(max_length=50, blank=True)
    features = models.TextField(default='[]', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)
    tags = models.TextField(default='[]', blank=True)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPES, default='single')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.name
    
    def get_image_url(self):
        """Return image URL, preferring uploaded image over URL"""
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return '/static/images/default-product.jpg'

class SiteInfo(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    description = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    hours = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    whatsapp = models.URLField(blank=True)
    success_rate = models.CharField(max_length=10, default='95%')
    happy_customers = models.CharField(max_length=20, default='50,000+')
    years_experience = models.CharField(max_length=10, default='10+')
    logo_url = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Site Info"
        verbose_name_plural = "Site Info"
    
    def __str__(self):
        return self.name

class Certification(models.Model):
    site = models.ForeignKey(SiteInfo, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.user.email}"

class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('paid', 'Paid'),
    ]
    
    PAYMENT_METHODS = [
        ('cod', 'Cash on Delivery'),
        ('razorpay', 'Razorpay'),
        ('other', 'Other'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True)
    payment_id = models.CharField(max_length=100, blank=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    order_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_total(self):
        return self.quantity * self.price
