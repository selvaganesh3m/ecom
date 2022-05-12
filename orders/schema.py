import graphene
from graphql import GraphQLError

from .models import Order, OrderItem
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem


class OrderQuery(graphene.ObjectType):
    get_my_orders = graphene.List(OrderType)

    @login_required
    def resolve_get_my_orders(self, info):
        user = info.context.user
        if user.is_authenticated:
            orders = Order.objects.filter(user=user)
            if not orders.count():
                raise GraphQLError("Your Don't have any orders")
            return orders
        return Order.objects.none()



