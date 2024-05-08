from django.apps import AppConfig


class MetricDetailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'metric_details'
    
    def ready(self):
        import metric_details.signals