import graphene
import graphql
from graphene_django.types import DjangoObjectType, ObjectType
from manual_matching.models import FinalMatching, ManualMatchingData
from directory.models import SyncEAS, SyncSKU, Competitors
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Value, CharField


class ClientDirectoryType(DjangoObjectType):
    class Meta:
        model = SyncSKU
        fields = ("id", "sku_id", "name")


class CompetitorsType(DjangoObjectType):
    class Meta:
        model = Competitors
        fields = ("name", "pharmacy_id", "firm_id")


class BaseDirectoryType(DjangoObjectType):
    class Meta:
        model = SyncEAS
        fields = ("id", "eas_id", "tn_fv")


class FinalMatchingType(DjangoObjectType):
    class Meta:
        model = FinalMatching
        fields = (
            'id', 'sku_dict', 'eas_dict', 'type_binding', 'name_binding', 'number_competitor', 'create_date',
            'update_date')


class ManualMatchingDataType(DjangoObjectType):
    class Meta:
        model = ManualMatchingData
        fields = ('id', 'sku_dict', 'number_competitor')

    """Данные поля используются для выгрузки вариантов мэтчинга ЕАС"""
    eas_ids = graphene.String()
    eas_names = graphene.String()


class Query(ObjectType):
    matching_all = graphene.List(
        FinalMatchingType,
        page=graphene.Int(),
        count=graphene.Int()
    )
    matching_filter = graphene.List(
        FinalMatchingType, type_binding=graphene.Int(),
        number_competitor=graphene.Int(),
        page=graphene.Int(),
        count=graphene.Int()
    )

    grocery = graphene.List(
        ManualMatchingDataType,
        pharmacy_id=graphene.Int(),
        firm_id=graphene.Int(),
        page=graphene.Int(),
        count=graphene.Int()
    )

    competitors = graphene.List(CompetitorsType)
    competitors_get = graphene.Field(CompetitorsType, id=graphene.Int(),)

    def resolve_competitors(self, info):
        """Список справочников"""
        return Competitors.objects.all()

    def resolve_competitors_get(self, info, id):
        """Получить справочник по внутреннему id Федора"""
        comp = Competitors.objects.get(pk=id)
        return comp

    def resolve_matching_all(self, info, count=500, page=1):
        """Результат мэтчинга в Федоре"""
        match = FinalMatching.objects.all()
        paginator = Paginator(match, count)
        try:
            res = paginator.page(page)
        except PageNotAnInteger:
            res = None
        except EmptyPage:
            res = None
        return res

    def resolve_matching_filter(self, info, type_binding, number_competitor, page=1, count=500):
        """Результат мэтчинга в Федоре"""
        match = FinalMatching.objects.filter(type_binding=type_binding, number_competitor=number_competitor)
        paginator = Paginator(match, count)
        try:
            res = paginator.page(page)
        except PageNotAnInteger:
            res = None
        except EmptyPage:
            res = None
        return res

    def resolve_grocery(self, info, pharmacy_id, firm_id, page=1, count=500):
        """Мэтчинг для аптек"""
        sku = ManualMatchingData.objects.filter(  # Список СКУ с пустыми доп полями, т.к. таблица денормализована
            sku_dict__number_competitor__pharmacy_id=pharmacy_id,
            sku_dict__number_competitor__firm_id=firm_id,
            matching_status=False).order_by('sku_dict__name', 'sku_dict__pk', ).annotate(
            eas_ids=Value('', output_field=CharField()),
            eas_names=Value('', output_field=CharField())
        ).distinct('sku_dict__name', 'sku_dict__pk')
        paginator = Paginator(sku, count)

        def custom_qwe(pk):
            """Функция для получения вариантов мэтчинга в ЕАС"""
            eas = ManualMatchingData.objects.filter(sku_dict__pk=pk).values(
                'eas_dict__eas_id',
                'name_eas'
            )
            eas_ids = []
            eas_names = []
            for ea in eas:
                eas_ids.append(ea['eas_dict__eas_id'])
                eas_names.append(ea['name_eas'])
            return str(eas_ids), str(eas_names)

        try:
            sku_list = paginator.page(page)
            for sk in sku_list:
                sk.eas_ids, sk.eas_names = custom_qwe(sk.sku_dict.pk)  # Зполнение доп. полей
            res = sku_list
        except PageNotAnInteger:
            res = None
        except EmptyPage:
            res = None
        return res
