from django.conf import settings


def get_log_settings():
    log = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': 'level:{levelname} time:{asctime} name:{name} message:{message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'filters': ['require_debug_true'],
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'fedor': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'auth_fedor': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'admin_panel': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'auto_matching': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'manual_matching': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            }
        },
    }
    return log
