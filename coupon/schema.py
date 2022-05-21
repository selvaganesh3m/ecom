import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Coupon


class CouponType(DjangoObjectType):
    class Meta:
        model = Coupon


class CouponQuery(graphene.ObjectType):
    get_active_coupons = graphene.List(CouponType)
    get_active_coupon = graphene.Field(CouponType, id=graphene.ID())

    def resolve_get_active_coupons(self, info, **kwargs):
        return Coupon.objects.all()

    def resolve_get_active_coupon(self, info, id):
        try:
            return Coupon.objects.get(id=id)
        except Coupon.DoesNotExist:
            return GraphQLError("Coupon doesn't exist")
