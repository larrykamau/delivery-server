import graphene

from ...account import error_codes as account_error_codes
from ...core import JobStatus, error_codes as core_error_codes
from ...core.permissions import get_permissions_enum_list
from ...core.weight import WeightUnits
from ...order import error_codes as order_error_codes
from .utils import str_to_enum

# FIXME CoreTaxRateType should be removed after we will drop old api fields dedicated
#  to taxes


class OrderDirection(graphene.Enum):
    ASC = ""
    DESC = "-"

    @property
    def description(self):
        # Disable all the no-member violations in this function
        # pylint: disable=no-member
        if self == OrderDirection.ASC:
            return "Specifies an ascending sort order."
        if self == OrderDirection.DESC:
            return "Specifies a descending sort order."
        raise ValueError("Unsupported enum value: %s" % self.value)


class ReportingPeriod(graphene.Enum):
    TODAY = "TODAY"
    THIS_MONTH = "THIS_MONTH"


def to_enum(enum_cls, *, type_name=None, **options) -> graphene.Enum:
    """Create a Graphene enum from a class containing a set of options.

    :param enum_cls:
        The class to build the enum from.
    :param type_name:
        The name of the type. Default is the class name + 'Enum'.
    :param options:
        - description:
            Contains the type description (default is the class's docstring)
        - deprecation_reason:
            Contains the deprecation reason.
            The default is enum_cls.__deprecation_reason__ or None.
    :return:
    """

    # note this won't work until
    # https://github.com/graphql-python/graphene/issues/956 is fixed
    deprecation_reason = getattr(enum_cls, "__deprecation_reason__", None)
    if deprecation_reason:
        options.setdefault("deprecation_reason", deprecation_reason)

    type_name = type_name or (enum_cls.__name__ + "Enum")
    enum_data = [(str_to_enum(code.upper()), code) for code, name in enum_cls.CHOICES]
    return graphene.Enum(type_name, enum_data, **options)


# TaxRateType = graphene.Enum(
#     "TaxRateType", [(str_to_enum(rate[0]), rate[0]) for rate in CoreTaxRateType.CHOICES]
# )

JobStatusEnum = to_enum(JobStatus)
PermissionEnum = graphene.Enum("PermissionEnum", get_permissions_enum_list())
WeightUnitsEnum = graphene.Enum(
    "WeightUnitsEnum", [(str_to_enum(unit[0]), unit[0]) for unit in WeightUnits.CHOICES]
)


AccountErrorCode = graphene.Enum.from_enum(account_error_codes.AccountErrorCode)
MetadataErrorCode = graphene.Enum.from_enum(core_error_codes.MetadataErrorCode)
OrderErrorCode = graphene.Enum.from_enum(order_error_codes.OrderErrorCode)
PermissionGroupErrorCode = graphene.Enum.from_enum(
    account_error_codes.PermissionGroupErrorCode
)
