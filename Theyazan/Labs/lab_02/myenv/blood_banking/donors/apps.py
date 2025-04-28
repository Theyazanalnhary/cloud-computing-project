from django.apps import AppConfig


class DonorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'donors'

# apps.py في تطبيق التبرعات

class DonationsConfig(AppConfig):
    name = 'donations'

    def ready(self):
        import donations.signals  # استيراد الإشارات
