from django.contrib import admin
from .models import Category, Product, SiteInfo, Certification, Review, ReviewLike, ReviewComment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    prepopulated_fields = {'id': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'sub_category', 'price', 'available', 'product_type']
    list_filter = ['category', 'available', 'product_type']
    search_fields = ['name', 'description', 'tags']
    prepopulated_fields = {'slug': ('name',)}

class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 1

@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    inlines = [CertificationInline]

class ReviewLikeInline(admin.TabularInline):
    model = ReviewLike
    extra = 0
    readonly_fields = ['ip_address', 'created_at']

class ReviewCommentInline(admin.TabularInline):
    model = ReviewComment
    extra = 0
    readonly_fields = ['ip_address', 'created_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'title', 'rating', 'is_approved', 'is_anonymous', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_anonymous', 'created_at']
    search_fields = ['name', 'email', 'title', 'content']
    list_editable = ['is_approved']
    actions = ['approve_reviews', 'disapprove_reviews']
    inlines = [ReviewCommentInline]
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} reviews approved successfully.')
    approve_reviews.short_description = 'Approve selected reviews'
    
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} reviews disapproved successfully.')
    disapprove_reviews.short_description = 'Disapprove selected reviews'

@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    list_display = ['review', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['review__title', 'ip_address']

@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ['review', 'name', 'content', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['review__title', 'name', 'content']
