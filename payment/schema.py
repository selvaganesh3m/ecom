import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from .models import Payment


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment


class PaymentQuery(object):
    payment = graphene.Field(PaymentType, order_id=graphene.ID())

    @login_required
    def resolve_payment(self, info, order_id):
        try:
            return Payment.objects.get(order=order_id)
        except Payment.DoesNotExist:
            return Payment.objects.none()
        except Payment.MultipleObjectsReturned:
            return Payment.objects.filter(order=order_id).last()


