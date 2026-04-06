from django.shortcuts import render, get_object_or_404
from .models import Product, Category, SiteInfo

def home(request):
    site_info = SiteInfo.objects.first()
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)[:8]
    return render(request, 'store/home.html', {
        'site_info': site_info,
        'categories': categories,
        'products': products,
    })

def products(request):
    site_info = SiteInfo.objects.first()
    category_filter = request.GET.get('category')
    search_query = request.GET.get('q')
    
    products_list = Product.objects.filter(available=True)
    
    if category_filter and category_filter != 'All':
        products_list = products_list.filter(category__name=category_filter)
    
    if search_query:
        products_list = products_list.filter(name__icontains=search_query)
    
    categories = Category.objects.all()
    
    return render(request, 'store/products.html', {
        'site_info': site_info,
        'products': products_list,
        'categories': categories,
        'category_filter': category_filter,
        'search_query': search_query,
    })

def product_detail(request, slug):
    site_info = SiteInfo.objects.first()
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    return render(request, 'store/product_detail.html', {
        'site_info': site_info,
        'product': product,
        'related_products': related_products,
    })

def about(request):
    site_info = SiteInfo.objects.first()
    return render(request, 'store/about.html', {
        'site_info': site_info,
        'site_name': site_info.name if site_info else 'Sugam Ayurveda',
        'site_about_us': site_info.description if site_info else 'Leading provider of natural Ayurvedic products',
        'site_company': site_info.company if site_info else 'Sugam Ayurveda',
    })

def contact(request):
    site_info = SiteInfo.objects.first()
    return render(request, 'store/contact.html', {'site_info': site_info})

def privacy_policy(request):
    site_info = SiteInfo.objects.first()
    return render(request, 'store/privacy_policy.html', {'site_info': site_info})

def terms_and_conditions(request):
    site_info = SiteInfo.objects.first()
    return render(request, 'store/terms_and_conditions.html', {'site_info': site_info})

def shipping_policy(request):
    site_info = SiteInfo.objects.first()
    return render(request, 'store/shipping_policy.html', {'site_info': site_info})

def return_policy(request):
    site_info = SiteInfo.objects.first()
    return render(request, 'store/return_policy.html', {'site_info': site_info})
