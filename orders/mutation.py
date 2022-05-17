import graphene
import razorpay
from django.conf import settings
from graphql import GraphQLError
import math
from cart.models import Cart
from .schema import OrderType
from payment.schema import PaymentType
from .models import Order, OrderItem
from payment.models import Payment

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class CreateOrderMutation(graphene.Mutation):
    order = graphene.Field(OrderType)
    payment = graphene.Field(PaymentType)

    def mutate(self, info):
        user = info.context.user
        if user.is_authenticated:
            try:
                cart = Cart.objects.get(user=user)
                cart_items = cart.cart_items.all()
                total = 0
                for cart_item in cart_items:
                    quantity = cart_item.quantity
                    product_price = cart_item.product.price
                    sub_total = quantity * product_price
                    total += sub_total
                order = Order.objects.create(
                    user=user,
                    shipping_address=cart.shipping_address,
                    billing_address=cart.billing_address,
                    total=total
                )
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                cart.delete()
                order_payment = client.order.create(dict(
                    currency='INR',
                    amount=int(round(math.ceil(order.total))),
                    payment_capture='1'
                ))
                payment = Payment.objects.create(
                    order=order,
                    user=user,
                    razorpay_order_id=order_payment['id']
                )
                print(order_payment)
                return CreateOrderMutation(order=order, payment=payment)
            except Cart.DoesNotExist:
                raise GraphQLError("User has No Active Order.")
        raise GraphQLError("Please Login")


class OrderMutation(graphene.ObjectType):
    create_order = CreateOrderMutation.Field()
