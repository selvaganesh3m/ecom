import graphene

from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserQuery(graphene.ObjectType):
    # User Detail
    user = graphene.Field(UserType, id=graphene.ID())
    # Users List
    users = graphene.List(UserType)

    @login_required
    def resolve_user(self, info, id):
        return get_user_model().objects.get(pk=id)

    @login_required
    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()
