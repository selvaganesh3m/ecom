from django.contrib import admin
from .models import Category, Product, ProductImage

admin.site.register(ProductImage)


class ProductInline(admin.StackedInline):
    model = Product
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
