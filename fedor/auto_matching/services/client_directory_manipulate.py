from auto_matching.models import ClientDirectory
from django.core import serializers
import logging, json

logger = logging.getLogger(__name__)


## @defgroup service_search_client_directory_data Сервис поиска по клиентскому справочнику
#  @brief search_client_directory
#  @ingroup search_client

## @ingroup service_search_client_directory_data
# @{
#  @param[in] data - поисковой запрос
#  @param[in] number_competitor - id клиента
#  @param[out] client_data = результат поиск по ClientDirectory
def search_client_directory(data, number_competitor_id):
    client_data = ClientDirectory.objects.filter(name__icontains=data,
                                                 joint_status=False,
                                                 number_competitor=number_competitor_id
                                                 )[:10]
    logger.debug(client_data)
    data = serializers.serialize('json', client_data)

    return data
##@}
