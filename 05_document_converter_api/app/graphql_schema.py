import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app import models


class ItemType(SQLAlchemyObjectType):
    """GraphQL Item type"""
    class Meta:
        model = models.Item


class Query(graphene.ObjectType):
    """GraphQL Query"""

    all_items = graphene.List(ItemType)
    item_by_id = graphene.Field(ItemType, id=graphene.Int(required=True))

    def resolve_all_items(self, info):
        return models.Item.query.all()

    def resolve_item_by_id(self, info, id):
        return models.Item.query.get(id)


class CreateItem(graphene.Mutation):
    """Create item mutation"""
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    item = graphene.Field(ItemType)

    @staticmethod
    def mutate(root, info, name, description=None):
        item = models.Item(name=name, description=description)
        # Save to database
        return CreateItem(item=item)


class UpdateItem(graphene.Mutation):
    """Update item mutation"""
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()

    item = graphene.Field(ItemType)

    @staticmethod
    def mutate(root, info, id, name=None, description=None):
        item = models.Item.query.get(id)
        if name:
            item.name = name
        if description:
            item.description = description
        # Save to database
        return UpdateItem(item=item)


class DeleteItem(graphene.Mutation):
    """Delete item mutation"""
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        item = models.Item.query.get(id)
        # Delete from database
        return DeleteItem(success=True)


class Mutation(graphene.ObjectType):
    """GraphQL Mutations"""
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()


# Create schema
schema = graphene.Schema(query=Query, mutation=Mutation)
