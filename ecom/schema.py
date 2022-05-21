import graphene

from cart.mutation import CartMutation
from cart.schema import CartQuery
from coupon.mutation import CouponMutation
from products.schema import Query
from products.mutation import Mutation
import graphql_jwt
from customers.schema import UserQuery
from customers.mutation import UserMutation
from graphql_jwt.refresh_token import mutations
from orders.schema import OrderQuery
from orders.mutation import OrderMutation
from payment.schema import PaymentQuery
from coupon.schema import CouponQuery


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(Query, UserQuery, CartQuery, OrderQuery, PaymentQuery, CouponQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, UserMutation, Mutation, CartMutation, OrderMutation, CouponMutation,graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
