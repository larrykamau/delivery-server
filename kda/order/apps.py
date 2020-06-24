from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrderConfig(AppConfig):
    name = "kda.order"
    verbose_name = _("Order")

    def ready(self):
        try:
            import kda.order.signals  # noqa F401
        except ImportError:
            pass
