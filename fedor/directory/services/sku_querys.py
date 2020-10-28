from directory.models import ClientDirectory

def test_get_sku(number_competitor):
    result = ClientDirectory.objects.filter(number_competitor=number_competitor, matching_status=False)[:30]
    return result

def change_matching_status_sku(sku):
    ClientDirectory.objects.filter(pk__in=[x.id for x in sku]).update(matching_status=True)
    return True