from directory.models import *
from django.core import serializers
from manual_matching.models import *


class Filter:

    def __init__(self, filter_matching):
        self.filter_matching = filter_matching

    def set_filter_matching(self, filter_matching):
        self.filter_matching = filter_matching

    def get_filter_matching(self):
        return self.filter_matching

    def business_logic(self, **fields):
        fm = self.get_filter_matching()
        result = fm.start(**fields)
        data = serializers.serialize('json', result)
        return data


class FilterManufacturer:

    def start(self, **fields):
        print(fields)
        res = ManualMatchingData.objects.filter(
            sku_dict__pk=fields['sku_id'],
            number_competitor=fields['number_competitor'],
            eas_dict__manufacturer=fields['manufacturer'],
            eas_dict__tn_fv=fields['tn_fv']

        )
        return res


if __name__ == '__main__':
    filter_match = Filter(FilterManufacturer())
    res = filter_match.business_logic(
        sku_id=666,
        number_competitor=2,
        eas_dict__manufacturer='burugaga',
        eas_dict__tn_fv='zelenka'
    )
    print(res)
