import graphene
from .schema import CategoryType
from .models import Category


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        slug = graphene.String()

    category = graphene.Field(CategoryType)

    def mutate(self, info, name, slug):
        category = Category.objects.create(
            name=name,
            slug=slug,
        )
        return CreateCategory(category=category)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
