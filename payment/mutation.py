import graphene
from graphene_django import DjangoObjectType

import razorpay
from django.conf import settings
from graphql import GraphQLError

from orders.models import Order
from orders.schema import OrderType




# class PayForOderMutation(graphene.Mutation):
#     class Arguments:
#         order_id = graphene.ID()
#
#     order = graphene.Field(OrderType)
#
#     def mutate(self, info, order_id):
#         try:
#             order = Order.objects.get(id=order_id)
#             razorpay_order = client.order.create(dict(amount=order.total,
#                                                       currency='INR',
#                                                       payment_capture='0'))
#             razorpay_order_id = razorpay_order['id']
#         except Order.DoesNotExist:
#             raise GraphQLError("Order Does not Exists")
#
#
# class PaymentMutation(graphene.ObjectType):
#     pay = PayForOderMutation.Field()
