from django.apps import AppConfig


class LeadConfig(AppConfig):
    name = 'LMS.lead'

    def ready(self):
        import LMS.lead.signals

