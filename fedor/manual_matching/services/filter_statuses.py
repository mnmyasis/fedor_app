from .filters import Filter
from manual_matching.models import *
import logging, json

logger = logging.getLogger(__name__)


class FilterStatuses:

    def start(self, **fields):
        filter_re = FinalMatching.objects.filter(
            number_competitor=fields['number_competitor'],
            user=fields['user_id'],
            type_binding__in=[status for status in fields['statuses']]).values(
                                                    'eas_dict__pk',
                                                    'eas_dict__tn_fv',
                                                    'sku_dict__name',
                                                    'sku_dict__pk',
                                                    'type_binding',
                                                    'name_binding',
                                                    'number_competitor'
                                                )
        filter_re = json.dumps(list(filter_re))
        filter_re = {'matching': filter_re}
        return filter_re
