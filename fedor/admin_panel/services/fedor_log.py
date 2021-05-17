from admin_panel.models import FedorLog


def log(message, user, action, sku_id=None, eas_id=None):
    print('###########################LOG#################################')
    print('user{} - message {} - action {} - sku_id {} - eas_id {}'.format(user, message, action, sku_id, eas_id))
    print('###########################LOG#################################')
    FedorLog.objects.create(
        user=user,
        message=message,
        action=action,
        sku_id=sku_id,
        eas_id=eas_id
    )