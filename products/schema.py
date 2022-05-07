import graphene
from graphene_django.types import DjangoObjectType
from .models import Product, Category, ProductImage


class ProductImageType(DjangoObjectType):
    image_url = graphene.String()

    class Meta:
        model = ProductImage

    def resolve_image_url(self, info):
        return info.context.build_absolute_uri(self.image)


class ProductType(DjangoObjectType):
    featured_image = graphene.String()

    class Meta:
        model = Product

    def resolve_featured_image(self, info):
        featured_image = self.images.filter(is_featured=True).first()
        return info.context.build_absolute_uri(featured_image)


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class Query(object):

    products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.ID())

    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.ID())

    def resolve_products(self, info, **kwargs):
        return Product.objects.filter(is_active=True)

    def resolve_product(self, info, id):
        return Product.objects.get(pk=id)

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_category(self, info, id):
        return Category.objects.get(pk=id)
