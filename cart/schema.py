import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Cart, CartItem


class CartType(DjangoObjectType):
    class Meta:
        model = Cart


class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem


class CartQuery(object):
    get_my_cart = graphene.List(CartType, id=graphene.ID(required=False), user_id=graphene.ID(required=False))

    def resolve_get_my_cart(self, info, **kwargs):
        if id := kwargs.get('id'):
            cart = Cart.objects.filter(id=id)
            if len(cart) == 0:
                return None
            return cart
        if user_id := kwargs.get('user_id'):
            cart = Cart.objects.filter(user__id=user_id)
            if len(cart) == 0:
                return None
            return cart