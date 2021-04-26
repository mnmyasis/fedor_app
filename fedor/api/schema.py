import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from manual_matching.models import FinalMatching
from directory.models import ClientDirectory, BaseDirectory, SyncEAS, SyncSKU


class ClientDirectoryType(DjangoObjectType):
    class Meta:
        model = SyncSKU
        fields = ("id", "sku_id", "name")


class BaseDirectoryType(DjangoObjectType):
    class Meta:
        model = SyncEAS
        fields = ("id", "eas_id", "tn_fv")


class FinalMatchingType(DjangoObjectType):
    class Meta:
        model = FinalMatching
        fields = ('sku_dict', 'eas_dict', 'type_binding', 'name_binding', 'number_competitor', 'create_date', 'update_date')


class Query(ObjectType):
    matching_all = graphene.List(FinalMatchingType)
    matching_filter = graphene.List(FinalMatchingType, type_binding=graphene.Int(), number_competitor=graphene.Int())

    def resolve_matching_all(self, info, **kwargs):
        return FinalMatching.objects.all()

    def resolve_matching_filter(self, info, type_binding, number_competitor):
        return FinalMatching.objects.filter(type_binding=type_binding, number_competitor=number_competitor)
