import graphene
from graphql import GraphQLError

from customers.models import UserAddress, User
from customers.schema import UserAddressType
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
        user = info.context.user
        if user.is_authenticated:
            try:
                cart = Cart.objects.get(user=user)
                try:
                    product = Product.objects.get(id=product_id)
                    try:
                        cart_item = CartItem.objects.get(cart=cart, product=product)
                    except CartItem.MultipleObjectsReturned:
                        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
                    except CartItem.DoesNotExist:
                        raise GraphQLError("Product is not in the cart")
                    cart_item.delete()
                    return RemoveFromCartMutation(cart=cart)
                except Product.DoesNotExist:
                    raise GraphQLError("Product is not in your cart to remove")
            except Cart.DoesNotExist:
                raise GraphQLError('User has no Cart')
        try:
            cart = Cart.objects.get(id=cart_id)
            try:
                product = Product.objects.get(id=product_id)
                try:
                    cart_item = CartItem.objects.get(cart=cart, product=product)
                except CartItem.MultipleObjectsReturned:
                    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
                except CartItem.DoesNotExist:
                    raise GraphQLError("Product is not in the cart")
                cart_item.delete()
                return RemoveFromCartMutation(cart=cart)
            except Product.DoesNotExist:
                raise GraphQLError("Product is not in your cart to remove")
        except Cart.DoesNotExist:
            raise GraphQLError("Cart unavailable")


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
            # try:
            #     user_cart = user.cart
            #     try:
            #         cart = Cart.objects.get(pk=cart_id)
            #         cart_items = user_cart.cart_items.all()
            #         user_cart_items = user_cart.cart_items.all()
            #     except Cart.DoesNotExist:
            #         raise GraphQLError("Cart does not exist.")
            # except Cart.DoesNotExist:
            #     raise GraphQLError("User has no cart.")
            try:
                user_cart = user.cart
                try:
                    cart = Cart.objects.get(pk=cart_id)
                    cart_items = cart.cart_items.all()
                    user_cart_items = user_cart.cart_items.all()
                    same_products = []
                    c_items = []
                    for cart_item in cart_items:
                        for user_cart_item in user_cart_items:
                            if cart_item.product.id == user_cart_item.product.id:
                                quantity = cart_item.quantity + user_cart_item.quantity
                                same_products.append((cart_item, quantity))
                                user_cart_item.delete()
                            c_items.append(cart_item)
                    for c_item in c_items:
                        c_item.cart = user_cart
                    CartItem.objects.bulk_update(c_items, ['cart'])
                    cart_it = []
                    for same_product in same_products:
                        same_product[0].quantity = same_product[1]
                        cart_it.append(same_product[0])
                    CartItem.objects.bulk_update(cart_it, ['quantity'])
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



class ChooseDeliveryAddressMutation(graphene.Mutation):
    class Arguments:
        shipping_addr_id = graphene.ID()
        billing_addr_id = graphene.ID()

    cart = graphene.Field(CartType)

    def mutate(self, info, billing_addr_id, shipping_addr_id):
        user = info.context.user
        if user.is_authenticated:
            try:
                cart = Cart.objects.get(user=user)
                try:
                    billing_address = UserAddress.objects.get(id=billing_addr_id)
                    cart.billing_address = billing_address
                    cart.save()
                except UserAddress.DoesNotExist:
                    raise GraphQLError("UserAddress Does not Exist.")
                try:
                    shipping_address = UserAddress.objects.get(id=shipping_addr_id)
                    cart.shipping_address = shipping_address
                    cart.save()
                except UserAddress.DoesNotExist:
                    raise GraphQLError("UserAddress Does not Exist.")
                return ChooseDeliveryAddressMutation(cart=cart)
            except Cart.DoesNotExist:
                raise GraphQLError("User Has No cart")
        raise GraphQLError("Please Login")


class CartMutation(graphene.ObjectType):
    add_to_cart = AddToCartMutation.Field()
    remove_from_cart = RemoveFromCartMutation.Field()

    # attaches the cart with the user
    cart_attachment = CartAttachmentMutation.Field()

    # choose delivery address mutation
    choose_delivery_address = ChooseDeliveryAddressMutation.Field()
