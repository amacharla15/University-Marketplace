# app1/apps.py
from django.apps import AppConfig

class App1Config(AppConfig):
    name = "university_marketplace.app1"

    def ready(self):
       
        import university_marketplace.app1.signals  # type: ignore
