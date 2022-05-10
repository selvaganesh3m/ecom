import graphene

from cart.mutation import CartMutation
from cart.schema import CartQuery
from products.schema import Query
from products.mutation import Mutation
import graphql_jwt
from customers.schema import UserQuery
from customers.mutation import UserMutation
from graphql_jwt.refresh_token import mutations


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(Query, UserQuery, CartQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, UserMutation, Mutation, CartMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
