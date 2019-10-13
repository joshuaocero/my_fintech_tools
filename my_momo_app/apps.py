from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MyMomoAppConfig(AppConfig):
    name = 'my_momo_app'
    verbose_name = _('my_momo_app')

    def ready(self):
        import my_momo_app.signals
