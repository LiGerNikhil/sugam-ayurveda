from django.contrib import admin
from .models import Category, Product, SiteInfo, Certification

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
