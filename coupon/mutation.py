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

    def mutate(self, info, coupon):
        user = info.context.user
        if user.is_authenticated:
            try:
                coupon = Coupon.objects.get(code__exact=coupon)
                if CouponUser.objects.filter(user=user, coupon=coupon).exists():
                    raise GraphQLError('Coupon Already Used by the User.')
                if coupon.expiry_date < timezone.now().date():
                    raise GraphQLError('Coupon Expired.')
                if coupon.activated_date > timezone.now().date():
                    raise GraphQLError('Coupon Not Activated.')
                try:
                    cart = Cart.objects.get(user=user)
                    if cart.coupon_applied:
                        raise GraphQLError("Coupon Already Applied.")
                    if not cart.coupon_applied or cart.grand_total == calculate_grand_total(cart):
                        cart.grand_total = calculate_grand_total(cart)
                        discount_calc_value = (coupon.percentage / 100) * float(cart.grand_total)
                        if discount_calc_value > coupon.max_discount_price:
                            cart.grand_total -= decimal.Decimal(coupon.max_discount_price)
                        else:
                            cart.grand_total -= decimal.Decimal(discount_calc_value)
                        cart.coupon_applied = True
                        cart.coupon = coupon
                        cart.save()
                    return ApplyCoupon(cart=cart)
                except Cart.DoesNotExist:
                    raise GraphQLError('User has no Cart')
            except Coupon.DoesNotExist:
                raise GraphQLError('Coupon Invalid')


class RemoveCoupon(graphene.Mutation):
    cart = graphene.Field(CartType)

    def mutate(self, info):
        user = info.context.user
        if user.is_authenticated:
            try:
                cart = Cart.objects.get(user=user)
                cart.coupon_applied = False
                cart.coupon = None
                cart.grand_total = calculate_grand_total(cart)
                cart.save()
                return RemoveCoupon(cart=cart)
            except Cart.DoesNotExist:
                raise GraphQLError('Cart Does not exist')


class CouponMutation(graphene.ObjectType):
    apply_coupon = ApplyCoupon.Field()
    remove_coupon = RemoveCoupon.Field()
