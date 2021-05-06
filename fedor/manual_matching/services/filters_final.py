from manual_matching.models import *
import logging, json
from django.db.models import Q

logger = logging.getLogger(__name__)


class FilterStatuses:

    def __init__(self):
        self.competitors = ''
        self.user_id = ''
        self.statuses = ''
        self.sku_form = ''
        self.eas_form = ''

    def filter_statuses(self):
        """Поиск только по статусам"""
        filter_re = FinalMatching.objects.filter(
            Q(number_competitor__in=self.competitors,
              type_binding__in=[status for status in self.statuses if int(status) in (2, 8)]) |
            Q(number_competitor__in=self.competitors,
              user=self.user_id,
              type_binding__in=[status for status in self.statuses if int(status) not in (2, 8)])

        ).order_by('sku_dict__name', 'number_competitor').values(
            'eas_dict__pk',
            'eas_dict__tn_fv',
            'sku_dict__name',
            'sku_dict__pk',
            'type_binding',
            'name_binding',
            'number_competitor'
        )
        return filter_re

    def filter_sku_and_eas(self):
        """Поиск с учетом статусов,ску,еас форм"""
        sku_eas = {}
        if self.sku_form and self.eas_form:
            sku_eas = {
                'sku_dict__name__icontains': self.sku_form,
                'eas_dict__tn_fv__icontains': self.eas_form
            }
        elif self.sku_form:
            sku_eas = {
                'sku_dict__name__icontains': self.sku_form,
            }
        elif self.eas_form:
            sku_eas = {
                'eas_dict__tn_fv__icontains': self.eas_form,
            }
        if len(self.statuses) > 0:  # Поиск с учетом статуса мэтчинга, если он выбран
            filter_re = FinalMatching.objects.filter(
                number_competitor__in=self.competitors,
                type_binding__in=self.statuses,
                **sku_eas
            ).values(
                'eas_dict__pk',
                'eas_dict__tn_fv',
                'sku_dict__name',
                'sku_dict__pk',
                'type_binding',
                'name_binding',
                'number_competitor'
            )
        else:  # Если статус не выбран, поиск без его учета
            filter_re = FinalMatching.objects.filter(
                number_competitor__in=self.competitors,
                **sku_eas
            ).values(
                'eas_dict__pk',
                'eas_dict__tn_fv',
                'sku_dict__name',
                'sku_dict__pk',
                'type_binding',
                'name_binding',
                'number_competitor'
            )
        return filter_re

    def start(self, **fields):
        self.competitors = fields.get('number_competitor')
        self.user_id = fields.get('user_id')
        self.statuses = fields.get('statuses')
        self.sku_form = fields.get('sku_form')
        self.eas_form = fields.get('eas_form')
        """Поиск с учетом статусов,ску,еас форм"""
        if len(self.statuses) > 0 and not self.sku_form and not self.eas_form:
            filter_re = self.filter_statuses()
        else:
            """Поиск с учетом статусов,ску,еас форм"""
            filter_re = self.filter_sku_and_eas()
        filter_re = json.dumps(list(filter_re))
        filter_re = {'matching': filter_re}
        return filter_re
