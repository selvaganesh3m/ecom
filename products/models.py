from django.db import models


# 3 models
# Category, Product, ProductImage

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=150)
    slug = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.PositiveIntegerField(null=True, blank=True)  # in percentage
    sku = models.CharField(max_length=100, unique=True)
    stock = models.PositiveIntegerField()  # total unit of product
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.sku


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='images/')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.image.path
