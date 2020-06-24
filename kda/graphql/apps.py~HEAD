from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GraphqlConfig(AppConfig):
    name = "kda.graphql"
    verbose_name = _("Graphql")

    def ready(self):
        try:
            import kda.graphql.signals  # noqa F401
        except ImportError:
            pass
