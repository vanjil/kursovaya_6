from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')

# Создаем объект Celery
app = Celery('mailing')

# Загрузка настроек из файла settings.py с префиксом CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в приложениях Django
app.autodiscover_tasks()

# Функция для обеспечения совместимости с Django 3.2 и ниже
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
