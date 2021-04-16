"""
WSGI config for fedor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
#/home/mnmyasis/dev/fedor_app/fedor/fedor
sys.path.append('/home/mnmyasis/dev/fedor_app/fedor')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fedor.settings')

application = get_wsgi_application()
