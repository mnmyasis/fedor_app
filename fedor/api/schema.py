import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from manual_matching.models import FinalMatching
from directory.models import ClientDirectory, BaseDirectory, SyncEAS, SyncSKU
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
        fields = ('id', 'sku_dict', 'eas_dict', 'type_binding', 'name_binding', 'number_competitor', 'create_date', 'update_date')


class Query(ObjectType):
    matching_all = graphene.List(FinalMatchingType, page=graphene.Int())
    matching_filter = graphene.List(FinalMatchingType, type_binding=graphene.Int(), number_competitor=graphene.Int(), page=graphene.Int())

    def resolve_matching_all(self, info, page=1):
        match = FinalMatching.objects.all()
        paginator = Paginator(match, 500)
        try:
            res = paginator.page(page)
        except PageNotAnInteger:
            res = None
        except EmptyPage:
            res = None
        return res

    def resolve_matching_filter(self, info, type_binding, number_competitor, page=1):
        match = FinalMatching.objects.filter(type_binding=type_binding, number_competitor=number_competitor)
        paginator = Paginator(match, 500)
        try:
            res = paginator.page(page)
        except PageNotAnInteger:
            res = None
        except EmptyPage:
            res = None
        return res
