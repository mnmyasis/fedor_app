from directory.models import SyncEAS, SyncSKU, Competitors
from python_graphql_client import GraphqlClient


def request_eas_api():
    """Синхронизация базовго справочника"""
    client = GraphqlClient(endpoint="http://test.eas.content.pharma.global/api")
    query = """query($status: Int!, $page: Int, $count: Int){
                            eas_product(status: $status, page: $page, count: $count){
                            id,
                            name_base,
                            is_registration,
                            corporation{
                              name
                            },
                            manufacturer{
                              name
                            },
                            type{
                              name
                            },
                            tradename{
                              name,
                              umbrella
                            },
                            iqvia_id,
                            packaging,
                            ddd,
                            weight_volume,
                            numero,
                            taste,
                            vendor_code,
                            split,
                            size,
                            age,
                            status{
                              id
                            },
                             ean{
                              value,
                            }
                        }
                    }"""
    statuses = [1, 3]
    for status in statuses:
        api_status = True
        page = 0
        while api_status:
            variables = {"status": status, 'page': page, 'count': 500}
            data = client.execute(query=query, variables=variables)
            eas_list = data.get('data').get('eas_product')
            if eas_list:
                for eas_data in eas_list:
                    print('page: {}'.format(page))
                    eas_wr = {}
                    eas_wr['eas_id'] = eas_data.get('id')
                    eas_wr['umbrella_brand'] = eas_data.get('tradename').get('umbrella')
                    eas_wr['tn_fv'] = eas_data.get('name_base')
                    eas_wr['registration_tm'] = eas_data.get('is_registration')
                    eas_wr['corporation'] = eas_data.get('corporation').get('name')
                    eas_wr['manufacturer'] = eas_data.get('manufacturer').get('name')
                    eas_wr['rx_otc'] = eas_data.get('type').get('name')
                    eas_wr['trade_name_rus'] = eas_data.get('tradename').get('name')
                    eas_wr['trade_name_eng'] = None
                    eas_wr['pack_key'] = eas_data.get('iqvia_id')
                    eas_wr['fv_short'] = None
                    eas_wr['type_packing_fv'] = eas_data.get('packaging')
                    eas_wr['dosage'] = eas_data.get('ddd')
                    eas_wr['volwe'] = eas_data.get('weight_volume')
                    eas_wr['numero'] = eas_data.get('numero')
                    eas_wr['tastes_and_parentheses_fv'] = eas_data.get('taste')
                    eas_wr['vendor_code'] = eas_data.get('vendor_code')
                    eas_wr['divisible_packaging'] = eas_data.get('split')
                    eas_wr['size'] = eas_data.get('size')
                    eas_wr['age'] = eas_data.get('age')
                    eas_wr['full_corp'] = "{} {}".format(eas_data.get(
                        'corporation').get('name'), eas_data.get('manufacturer').get('name'))
                    eas_wr['corp_rus'] = None
                    eas_wr['status'] = eas_data.get('status').get('id')
                    barcode = []
                    for br_code in eas_data.get('ean'):
                        barcode.append(br_code.get('value'))
                    eas_wr['barcode'] = str(barcode)
                    s_eas, s_status = SyncEAS.objects.update_or_create(**eas_wr, defaults=eas_wr)
                page += 1
            else:
                api_status = False
    return True


def request_sku_api():
    """Синхронизация клиентских справочников"""
    client = GraphqlClient(endpoint="https://rio.pharma.global/graphql-local")
    query = """
        query($limit: Int){
          good(limit: $limit, where: {product_match_status: null}){
            id,
            product_id,
            pharmacy_id,
            firm_id,
            name,
            producer,
            ean
          }
        }
    """
    variables = {}
    data = client.execute(query=query, variables=variables)
    sku_list = data.get('data').get('good')
    for sku_data in sku_list:
        sku_wr = {}
        competitor = {}
        sku_wr['sku_id'] = sku_data.get('id')
        sku_wr['name'] = "{} {}".format(sku_data.get('name'), sku_data.get('producer'))
        competitor['pharmacy_id'] = sku_data.get('pharmacy_id')
        competitor['firm_id'] = sku_data.get('firm_id')
        competitor['name'] = 'test pharmacy_id-{} firm_id-{}'.format(sku_data.get('pharmacy_id'), sku_data.get('firm_id'))
        sku_wr['nnt'] = sku_data.get('ean')
        number_competitor, created = Competitors.objects.get_or_create(**competitor, defaults=competitor)
        sku_wr['number_competitor'] = number_competitor
        s_sku, s_status = SyncSKU.objects.update_or_create(
            name=sku_wr['name'],
            number_competitor=sku_wr['number_competitor'],
            defaults=sku_wr)
        print(s_sku)
    return True
