from django.contrib import admin
from .models import Category, Product, ProductImage

admin.site.register(ProductImage)


class ProductInline(admin.TabularInline):
    model = Product


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
