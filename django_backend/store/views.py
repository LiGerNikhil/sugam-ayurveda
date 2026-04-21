from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.urls import reverse
from urllib.parse import urlencode
from .models import Product, Category, SiteInfo, Review, ReviewLike, ReviewComment
from .forms import ReviewForm, ReviewCommentForm

def home(request):
    site_info = SiteInfo.objects.first()
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)[:8]
    
    # Get approved reviews for homepage display
    approved_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')[:6]
    
    # Calculate rating statistics
    all_reviews = Review.objects.filter(is_approved=True)
    total_reviews = all_reviews.count()
    
    if total_reviews > 0:
        # Calculate average rating
        avg_rating = sum(review.rating for review in all_reviews) / total_reviews
        avg_rating = round(avg_rating, 1)
        
        # Calculate rating distribution
        rating_counts = []
        rating_percentages = []
        for i in range(1, 6):
            count = all_reviews.filter(rating=i).count()
            percentage = round((count / total_reviews) * 100, 0)
            rating_counts.append(count)
            rating_percentages.append(percentage)
    else:
        avg_rating = 0.0
        rating_counts = [0, 0, 0, 0, 0]
        rating_percentages = [0, 0, 0, 0, 0]
    
    # Get review form
    review_form = ReviewForm()
    
    return render(request, 'store/home.html', {
        'site_info': site_info,
        'categories': categories,
        'products': products,
        'approved_reviews': approved_reviews,
        'review_form': review_form,
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
        'rating_counts': rating_counts,
        'rating_percentages': rating_percentages,
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

def category_detail(request, slug):
    category = get_object_or_404(Category, id=slug)
    url = reverse('products')
    query = urlencode({'category': category.name})
    return redirect(f'{url}?{query}')

def product_detail(request, slug):
    site_info = SiteInfo.objects.first()
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    # Get approved reviews for this product
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')[:10]
    
    # Get review form
    review_form = ReviewForm()
    
    return render(request, 'store/product_detail.html', {
        'site_info': site_info,
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'review_form': review_form,
    })

def submit_review(request):
    """Handle review submission"""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            messages.success(request, 'Thank you for your review! Your review is now visible on the homepage.')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return redirect('home')

@require_POST
def like_review(request, review_id):
    """Handle review likes"""
    try:
        review = Review.objects.get(id=review_id, is_approved=True)
        ip_address = get_client_ip(request)
        
        # Check if already liked
        if not ReviewLike.objects.filter(review=review, ip_address=ip_address).exists():
            ReviewLike.objects.create(review=review, ip_address=ip_address)
            like_count = ReviewLike.objects.filter(review=review).count()
            return JsonResponse({'success': True, 'like_count': like_count})
        else:
            return JsonResponse({'success': False, 'message': 'You have already liked this review'})
    except Review.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Review not found'})

@require_POST
def comment_review(request, review_id):
    """Handle review comments"""
    try:
        review = Review.objects.get(id=review_id, is_approved=True)
        form = ReviewCommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.ip_address = get_client_ip(request)
            comment.save()
            
            # Return updated comments
            comments = ReviewComment.objects.filter(review=review).order_by('created_at')
            comments_html = render_to_string('store/partials/review_comments.html', {'comments': comments})
            return JsonResponse({'success': True, 'comments_html': comments_html})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    except Review.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Review not found'})

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
