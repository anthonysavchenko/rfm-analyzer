from django.apps import AppConfig


class BackgroundTaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rfm_analyzer.apps.background_task'
    verbose_name = 'Background Tasks'
