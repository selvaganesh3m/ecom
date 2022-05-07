import graphene
from graphql import GraphQLError

from .schema import CartType
from .models import Cart, CartItem
from products.models import Product


class AddToCartMutation(graphene.Mutation):
    class Arguments:
        cart_id = graphene.ID(required=False)
        product_id = graphene.ID()
        quantity = graphene.Int(required=False)

    cart = graphene.Field(CartType)

    def mutate(self, info, cart_id=None, product_id=None, quantity=None):
        cart, cart_created = Cart.objects.get_or_create(id=cart_id)
        product = Product.objects.get(pk=product_id)
        try:
            cart_item_cart = CartItem.objects.get(cart=cart, product=product)
            cart_item_cart.quantity += 1
            if quantity == 0:
                cart_item_cart.quantity = 1
            if quantity:
                cart_item_cart.quantity = quantity
            cart_item_cart.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(
                cart=cart,
                product=product,
            )
        return AddToCartMutation(cart=cart)


class RemoveFromCartMutation(graphene.Mutation):
    class Arguments:
        cart_id = graphene.ID()
        product_id = graphene.ID()

    cart = graphene.Field(CartType)

    def mutate(self, info, cart_id=None, product_id=None):
        cart = Cart.objects.get(id=cart_id)
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        return RemoveFromCartMutation(cart=cart)


class CartMutation(graphene.ObjectType):
    add_to_cart = AddToCartMutation.Field()
    remove_from_cart = RemoveFromCartMutation.Field()
