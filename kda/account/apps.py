from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountConfig(AppConfig):
    name = "kda.account"
    verbose_name = _("Account")

    def ready(self):
        try:
            import kda.users.signals  # noqa F401
        except ImportError:
            pass
