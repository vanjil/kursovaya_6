from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.module_loading import autodiscover_modules

class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self):
        # Импортировать функции после полной инициализации
        from .tasks import start
        scheduler = BackgroundScheduler()
        scheduler.add_job(start, 'interval', seconds=10)
        scheduler.start()
