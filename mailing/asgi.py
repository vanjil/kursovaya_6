"""
ASGI config for mailing project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.apps import AppConfig

class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'
    verbose_name = 'Рассылки'  # Имя, которое будет отображаться в админке


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')

application = get_asgi_application()
