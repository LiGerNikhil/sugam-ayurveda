from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django import forms
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Product, SiteInfo, Certification, Customer, Order, OrderItem

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Custom login required decorator for admin dashboard
def admin_login_required(view_func):
    decorated_view_func = login_required(view_func, login_url='/login/')
    return decorated_view_func

class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
        'placeholder': 'Username or Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
        'placeholder': 'Password'
    }))

def admin_login_view(request):
    """Custom admin login view"""
    if request.user.is_authenticated and is_admin(request.user):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None and is_admin(user):
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials or insufficient permissions.')
    else:
        form = AdminLoginForm()
    
    return render(request, 'admin/login.html', {'form': form})

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'sub_category', 'description', 'size', 
                 'features', 'price', 'available', 'tags', 'product_type', 'image', 'image_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'slug': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'sub_category': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'size': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'product_type': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'image': forms.FileInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'image_url': forms.URLInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'available': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image']
        widgets = {
            'id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Category ID (slug-friendly)'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Category Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Category Description',
                'rows': 4
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'accept': 'image/*'
            })
        }

@admin_login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Main admin dashboard with statistics and overview"""
    # Check if user accessed directly without proper login
    if not request.user.is_authenticated or not is_admin(request.user):
        return redirect('login')
    
    total_products = Product.objects.count()
    available_products = Product.objects.filter(available=True).count()
    total_categories = Category.objects.count()
    total_site_info = SiteInfo.objects.count()
    total_users = User.objects.count()
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    
    recent_products = Product.objects.order_by('-created_at')[:5]
    recent_orders = Order.objects.order_by('-created_at')[:5]
    categories_with_counts = Category.objects.annotate(product_count=Count('products'))
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'total_products': total_products,
        'available_products': available_products,
        'total_categories': total_categories,
        'total_site_info': total_site_info,
        'total_users': total_users,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'recent_products': recent_products,
        'recent_orders': recent_orders,
        'categories_with_counts': categories_with_counts,
        'recent_users': recent_users,
    }
    return render(request, 'admin/dashboard.html', context)

@admin_login_required
@user_passes_test(is_admin)
def admin_products(request):
    """Manage products"""
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    category_filter = request.GET.get('category')
    search_query = request.GET.get('q')
    
    if category_filter:
        products = products.filter(category__id=category_filter)
    
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    context = {
        'products': products,
        'categories': categories,
        'category_filter': category_filter,
        'search_query': search_query,
    }
    return render(request, 'admin/products.html', context)

@admin_login_required
@user_passes_test(is_admin)
def admin_categories(request):
    """Manage categories"""
    categories = Category.objects.all().order_by('name')
    categories_with_counts = Category.objects.annotate(product_count=Count('products'))
    
    # Calculate statistics
    total_categories = categories_with_counts.count()
    most_products = 0
    total_products_in_categories = 0
    
    if categories_with_counts.exists():
        sorted_categories = sorted(categories_with_counts, key=lambda x: x.product_count, reverse=True)
        most_products = sorted_categories[0].product_count if sorted_categories else 0
        total_products_in_categories = sum(cat.product_count for cat in categories_with_counts)
    
    avg_products = total_products_in_categories / total_categories if total_categories > 0 else 0
    
    context = {
        'categories': categories_with_counts,
        'total_categories': total_categories,
        'most_products': most_products,
        'avg_products': avg_products,
    }
    return render(request, 'admin/categories.html', context)

@admin_login_required
@user_passes_test(is_admin)
def admin_site_info(request):
    """Manage site information"""
    site_info = SiteInfo.objects.first()
    
    if request.method == 'POST':
        if site_info:
            # Update existing site info
            site_info.name = request.POST.get('name', site_info.name)
            site_info.company = request.POST.get('company', site_info.company)
            site_info.tagline = request.POST.get('tagline', site_info.tagline)
            site_info.description = request.POST.get('description', site_info.description)
            site_info.phone = request.POST.get('phone', site_info.phone)
            site_info.email = request.POST.get('email', site_info.email)
            site_info.hours = request.POST.get('hours', site_info.hours)
            site_info.address = request.POST.get('address', site_info.address)
            site_info.facebook = request.POST.get('facebook', site_info.facebook)
            site_info.instagram = request.POST.get('instagram', site_info.instagram)
            site_info.youtube = request.POST.get('youtube', site_info.youtube)
            site_info.whatsapp = request.POST.get('whatsapp', site_info.whatsapp)
            site_info.success_rate = request.POST.get('success_rate', site_info.success_rate)
            site_info.happy_customers = request.POST.get('happy_customers', site_info.happy_customers)
            site_info.years_experience = request.POST.get('years_experience', site_info.years_experience)
            site_info.logo_url = request.POST.get('logo_url', site_info.logo_url)
            site_info.save()
        else:
            # Create new site info
            site_info = SiteInfo.objects.create(
                name=request.POST.get('name'),
                company=request.POST.get('company'),
                tagline=request.POST.get('tagline'),
                description=request.POST.get('description'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email'),
                hours=request.POST.get('hours'),
                address=request.POST.get('address'),
                facebook=request.POST.get('facebook'),
                instagram=request.POST.get('instagram'),
                youtube=request.POST.get('youtube'),
                whatsapp=request.POST.get('whatsapp'),
                success_rate=request.POST.get('success_rate'),
                happy_customers=request.POST.get('happy_customers'),
                years_experience=request.POST.get('years_experience'),
                logo_url=request.POST.get('logo_url'),
            )
        
        messages.success(request, 'Site information updated successfully!')
        return redirect('admin_site_info')
    
    context = {
        'site_info': site_info,
    }
    return render(request, 'admin/site_info.html', context)

@admin_login_required
@user_passes_test(is_admin)
def admin_stats(request):
    """Comprehensive statistics page"""
    from django.db.models import Count, Avg, Sum
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # Product Statistics
    total_products = Product.objects.count()
    available_products = Product.objects.filter(available=True).count()
    out_of_stock_products = Product.objects.filter(available=False).count()
    low_stock_products = Product.objects.filter(available=True).filter(
        size__icontains='tablet'  # Assuming low stock if size contains 'tablet'
    ).count() if Product.objects.filter(available=True).exists() else 0
    
    # Category Statistics
    total_categories = Category.objects.count()
    categories_with_products = Category.objects.annotate(product_count=Count('products')).filter(product_count__gt=0).count()
    empty_categories = total_categories - categories_with_products
    avg_products_per_category = Category.objects.annotate(product_count=Count('products')).aggregate(avg=Avg('product_count'))['avg'] or 0
    
    # Order Statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    processing_orders = Order.objects.filter(status='processing').count()
    shipped_orders = Order.objects.filter(status='shipped').count()
    delivered_orders = Order.objects.filter(status='delivered').count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()
    
    # Revenue Statistics
    total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    one_month_ago = timezone.now() - timedelta(days=30)
    revenue_this_month = Order.objects.filter(created_at__gte=one_month_ago).aggregate(total=Sum('total_amount'))['total'] or 0
    avg_order_value = Order.objects.aggregate(avg=Avg('total_amount'))['avg'] or 0
    
    # User Statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    inactive_users = User.objects.filter(is_active=False).count()
    admin_users = User.objects.filter(is_staff=True).count()
    
    # Recent Activity
    one_month_ago = timezone.now() - timedelta(days=30)
    new_users_this_month = User.objects.filter(date_joined__gte=one_month_ago).count()
    
    recent_orders = Order.objects.select_related('customer', 'customer__user').order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'stats': {
            'total_products': total_products,
            'available_products': available_products,
            'out_of_stock_products': out_of_stock_products,
            'low_stock_products': low_stock_products,
            'total_categories': total_categories,
            'categories_with_products': categories_with_products,
            'empty_categories': empty_categories,
            'avg_products_per_category': avg_products_per_category,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'processing_orders': processing_orders,
            'shipped_orders': shipped_orders,
            'delivered_orders': delivered_orders,
            'cancelled_orders': cancelled_orders,
            'total_revenue': total_revenue,
            'revenue_this_month': revenue_this_month,
            'avg_order_value': avg_order_value,
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'admin_users': admin_users,
            'new_users_this_month': new_users_this_month,
            'conversion_rate': round((delivered_orders / total_orders * 100) if total_orders > 0 else 0, 2),
        },
        'recent_orders': recent_orders,
        'recent_users': recent_users,
    }
    
    return render(request, 'admin/stats.html', context)

@admin_login_required
@user_passes_test(is_admin)
def admin_add_product(request):
    """Add new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('admin_products')
    else:
        form = ProductForm()
    
    return render(request, 'admin/product_form.html', {
        'form': form,
        'title': 'Add New Product',
        'action': 'Add'
    })

@admin_login_required
@user_passes_test(is_admin)
def admin_edit_product(request, product_id):
    """Edit existing product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'admin/product_form.html', {
        'form': form,
        'product': product,
        'title': 'Edit Product',
        'action': 'Update'
    })

@admin_login_required
@user_passes_test(is_admin)
def admin_add_category(request):
    """Add new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" added successfully!')
            return redirect('admin_categories')
    else:
        form = CategoryForm()
    
    return render(request, 'admin/category_form.html', {
        'form': form,
        'title': 'Add New Category',
        'action': 'Add'
    })

@admin_login_required
@user_passes_test(is_admin)
def admin_edit_category(request, category_id):
    """Edit existing category"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'admin/category_form.html', {
        'form': form,
        'category': category,
        'title': 'Edit Category',
        'action': 'Update'
    })

@admin_login_required
@user_passes_test(is_admin)
def admin_delete_category(request, category_id):
    """Delete category"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('admin_categories')
    
    return render(request, 'admin/category_delete.html', {
        'category': category
    })

@admin_login_required
@user_passes_test(is_admin)
def admin_users(request):
    """Manage users"""
    users = User.objects.all().order_by('-date_joined')
    
    search_query = request.GET.get('q')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'search_query': search_query,
    }
    return render(request, 'admin/users.html', context)

@admin_login_required
@user_passes_test(is_admin)
def admin_orders(request):
    """Manage orders"""
    orders = Order.objects.all().order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        orders = orders.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'admin/orders.html', context)

@csrf_exempt
@admin_login_required
@user_passes_test(is_admin)
def update_order_status(request, order_id):
    """Update order status"""
    print(f"DEBUG: update_order_status called with order_id={order_id}, method={request.method}")
    
    if request.method == 'POST':
        try:
            order = get_object_or_404(Order, id=order_id)
            new_status = request.POST.get('status')
            
            print(f"DEBUG: new_status={new_status}")
            
            if not new_status:
                return JsonResponse({
                    'success': False,
                    'message': 'Status is required'
                })
            
            # Validate status
            valid_statuses = [choice[0] for choice in Order.ORDER_STATUS]
            print(f"DEBUG: valid_statuses={valid_statuses}")
            
            if new_status not in valid_statuses:
                return JsonResponse({
                    'success': False,
                    'message': f'Invalid status. Valid options: {", ".join(valid_statuses)}'
                })
            
            # Update order
            old_status = order.status
            order.status = new_status
            order.save()
            
            print(f"DEBUG: Order status updated from {old_status} to {new_status}")
            
            return JsonResponse({
                'success': True,
                'old_status': old_status,
                'new_status': new_status,
                'message': f'Order status updated from {old_status} to {new_status}'
            })
            
        except Exception as e:
            print(f"DEBUG: Exception occurred: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Only POST requests are allowed'
    })

@admin_login_required
@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    """Toggle user active status"""
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()
        
        return JsonResponse({
            'success': True,
            'is_active': user.is_active,
            'message': f'User {"activated" if user.is_active else "deactivated"} successfully'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@admin_login_required
@user_passes_test(is_admin)
def update_order_status(request, order_id):
    """Update order status"""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        
        if new_status in ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']:
            order.status = new_status
            order.save()
            
            return JsonResponse({
                'success': True,
                'status': order.status,
                'message': f'Order status updated to {order.status}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@admin_login_required
@user_passes_test(is_admin)
def toggle_product_availability(request, product_id):
    """Toggle product availability status"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.available = not product.available
        product.save()
        
        return JsonResponse({
            'success': True,
            'available': product.available,
            'message': f'Product is now {"available" if product.available else "unavailable"}'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})
