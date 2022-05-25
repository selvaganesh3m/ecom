import graphene
from graphql import GraphQLError

from cart.models import Cart
from cart.schema import CartType
from django.utils import timezone

from cart.utils import calculate_grand_total
from coupon.models import Coupon, CouponUser
import decimal


class ApplyCoupon(graphene.Mutation):
    class Arguments:
        coupon = graphene.String()

    cart = graphene.Field(CartType)
    message = graphene.String()

    def mutate(self, info, coupon):
        user = info.context.user
        if user.is_authenticated:
            try:
                cart = Cart.objects.get(user=user)
                if cart.coupon:
                    raise GraphQLError('Coupon Already Applied.')
                try:
                    coupon = Coupon.objects.get(code__exact=coupon)
                    if CouponUser.objects.filter(user=user, coupon=coupon).exists():
                        raise GraphQLError('Coupon Already Used by the User.')
                    if coupon.expiry_date < timezone.now().date():
                        raise GraphQLError('Coupon Expired.')
                    if coupon.activated_date > timezone.now().date():
                        raise GraphQLError(f'Coupon will be activated from {coupon.activated_date}.')
                    cart_items = cart.cart_items.all()

                    # product based coupon apply
                    if coupon.coupon_type == 'PBO':
                        if not cart.coupon:
                            cart_items_equal = [cart_item for cart_item in cart_items if
                                                cart_item.product.title == coupon.product_name]
                            cart_items_total = [cart_item for cart_item in cart_items if
                                                cart_item.product.title == coupon.product_name if
                                                cart_item.total >= coupon.price_boundary]

                            cart_items_equal_length = len(cart_items_equal)
                            cart_items_total_length = len(cart_items_total)

                            if not cart_items_equal_length:
                                return ApplyCoupon(cart=cart, message=f'No {coupon.product_name} in cart to Apply '
                                                                      f'Coupon.')
                            cart.grand_total -= coupon.max_discount_price * cart_items_total_length
                            cart.coupon = coupon
                            cart.save()
                            return ApplyCoupon(cart=cart, message=(f'Coupon Applied for {cart_items_total_length} '
                                                                   f'{coupon.product_name} Product(s) only.'))
                        return ApplyCoupon(cart=cart, message='Coupon Already Applied.')

                    # category based coupon apply
                    if coupon.coupon_type == 'CBO':
                        if not cart.coupon:
                            cart_items_total = [cart_item for cart_item in
                                                cart_items.filter(product__category__name=coupon.category_name) if
                                                cart_item.total >= coupon.price_boundary]
                            cart_items_total_length = len(cart_items_total)
                            if not cart_items_total_length:
                                return ApplyCoupon(cart=cart, message=f'Cart has no item from {coupon.category_name}')
                            cart.grand_total -= coupon.max_discount_price * cart_items_total_length
                            cart.coupon = coupon
                            cart.save()
                            return ApplyCoupon(cart=cart, message=f'Coupon Applied for Products from '
                                                                  f'{coupon.category_name} Category')
                        return ApplyCoupon(cart=cart, message='Coupon Already Applied.')

                    # FLAT coupon offer
                    if coupon.coupon_type == 'FLO':
                        if not cart.coupon:
                            if cart.grand_total >= coupon.price_boundary:
                                cart.grand_total -= coupon.max_discount_price
                                cart.coupon = coupon
                                cart.save()
                                return ApplyCoupon(cart=cart, message=f'FLAT {coupon.max_discount_price}, '
                                                                      f'Coupon Applied.')
                            return ApplyCoupon(cart=cart, message=f'Cart total should be ${coupon.price_boundary} '
                                                                  f'or Higher')
                        return ApplyCoupon(cart=cart, message='Coupon Already Applied.')

                    # Percentage based offer
                    if coupon.coupon_type == 'PVO':
                        if not cart.coupon:
                            if cart.grand_total >= coupon.price_boundary:
                                discount_value = (coupon.percentage / 100) * float(cart.grand_total)
                                if discount_value <= coupon.max_discount_price:
                                    cart.grand_total -= discount_value
                                cart.grand_total -= coupon.max_discount_price
                                cart.coupon = coupon
                                cart.save()
                                return ApplyCoupon(cart=cart, message='Coupon Applied.')
                            return ApplyCoupon(cart=cart, message=f'Cart total should be ${coupon.price_boundary} '
                                                                  f'or Higher')
                        return ApplyCoupon(cart=cart, message='Coupon Already Applied.')

                    # Limited Coupon
                    if coupon.coupon_type == 'LCO':
                        if not cart.coupon:
                            if cart.grand_total >= coupon.price_boundary:
                                cart.grand_total -= coupon.max_discount_price
                                cart.coupon = coupon
                                cart.save()
                                return ApplyCoupon(cart=cart, message='Coupon Applied.')
                            return ApplyCoupon(cart=cart, message=f'Cart total should be ${coupon.price_boundary} '
                                                                  f'or Higher')
                        return ApplyCoupon(cart=cart, message='Coupon Already Applied.')
                except Coupon.DoesNotExist:
                    raise GraphQLError('Coupon Invalid.')
            except Cart.DoesNotExist:
                raise GraphQLError('Cart Does Not Exist')


class RemoveCoupon(graphene.Mutation):
    cart = graphene.Field(CartType)

    def mutate(self, info):
        user = info.context.user
        if user.is_authenticated:
            try:
                cart = Cart.objects.get(user=user)
                cart.coupon = None
                cart.grand_total = calculate_grand_total(cart)
                cart.save()
                return RemoveCoupon(cart=cart)
            except Cart.DoesNotExist:
                raise GraphQLError('Cart Does not exist')


class CouponMutation(graphene.ObjectType):
    apply_coupon = ApplyCoupon.Field()
    remove_coupon = RemoveCoupon.Field()
