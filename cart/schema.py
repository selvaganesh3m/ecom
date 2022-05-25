import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Cart, CartItem
from .utils import calculate_grand_total


class CartType(DjangoObjectType):
    class Meta:
        model = Cart
        field = '__all__'


class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem


class CartQuery(object):
    get_my_cart = graphene.List(CartType, cart_id=graphene.ID(required=False))

    def resolve_get_my_cart(self, info, **kwargs):
        user = info.context.user
        if id := kwargs.get('id'):
            carts = Cart.objects.filter(id=id)
            try:
                cart = carts.first()
                if cart:
                    if not cart.coupon:
                        cart.grand_total = calculate_grand_total(cart)
                        cart.save()
                return carts
            except Cart.DoesNotExist:
                return []

        if user.is_authenticated:
            carts = Cart.objects.filter(user=user)
            try:
                cart = carts.first()
                if cart:
                    if not cart.coupon:
                        cart.grand_total = calculate_grand_total(cart)
                        cart.save()
                return carts
            except Cart.DoesNotExist:
                return []




