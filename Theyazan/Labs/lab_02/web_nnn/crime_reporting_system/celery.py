from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crime_reporting_system.settings')

app = Celery('crime_reporting_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# جدولة المهام
app.conf.beat_schedule = {
    'send-daily-report': {
        'task': 'reports.tasks.send_daily_report',
        'schedule': 86400.0,  # كل 24 ساعة
    },
    'create-backup': {
        'task': 'crime_reporting_system.backup.create_backup',
        'schedule': 604800.0,  # كل أسبوع
    },
} 