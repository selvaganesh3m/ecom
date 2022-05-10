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
        user = info.context.user
        if user.is_authenticated:
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=user)
            # end-except
        else:
            try:
                cart = Cart.objects.get(pk=cart_id)
            except Cart.DoesNotExist:
                cart = Cart.objects.create()
            # end-except
        # endif
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise GraphQLError("Product Does not Exist.")
        # end-except

        try:
            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
            except CartItem.MultipleObjectsReturned:
                cart_item = CartItem.objects.filter(cart=cart, product=product).first()
            # end-except
            cart_item.quantity += 1
            if quantity == 0:
                cart_item.quantity = 1
            if quantity:
                cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(
                cart=cart,
                product=product,
            )
        # end-except
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


class CartAttachmentMutation(graphene.Mutation):
    """
    This Mutation will be associate the Anonymous user cart to Authenticated user
    """
    class Arguments:
        cart_id = graphene.ID()

    # returns logged in user
    cart = graphene.Field(CartType)

    def mutate(self, info, cart_id):
        user = info.context.user
        if user.is_authenticated:
            try:
                user_cart = Cart.objects.get(user=user)
                try:
                    cart = Cart.objects.get(pk=cart_id)
                    cart_items = CartItem.objects.filter(cart=cart)
                    user_cart_items = CartItem.objects.filter(cart=user_cart)
                    for cart_item in cart_items:
                        for user_cart_item in user_cart_items:
                            if cart_item.product.id == user_cart_item.product.id:
                                quantity = cart_item.quantity + user_cart_item.quantity
                                cart_item.quantity = quantity
                                cart_item.save()
                                user_cart_item.delete()
                            cart_item.cart = user_cart
                            cart_item.save()
                    return CartAttachmentMutation(cart=user_cart)
                except Cart.DoesNotExist:
                    raise GraphQLError("Cart Doesn't exist")
                # end-except
            except Cart.DoesNotExist:
                try:
                    cart = Cart.objects.get(pk=cart_id)
                    cart.user = user
                    cart.save()
                    return CartAttachmentMutation(cart=cart)
                except Cart.DoesNotExist:
                    raise GraphQLError("Cart Doesn't exist")
                # end-except
            # end-except




        








class CartMutation(graphene.ObjectType):
    add_to_cart = AddToCartMutation.Field()
    remove_from_cart = RemoveFromCartMutation.Field()

    # attaches the cart with the user
    cart_attachment = CartAttachmentMutation.Field()
