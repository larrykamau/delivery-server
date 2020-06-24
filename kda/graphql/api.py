from graphene_federation import build_schema

from .account.schema import AuthMutations #AccountMutations, AccountQueries, AuthMutations
# from .core.schema import CoreMutations, CoreQueries
# from .order.schema import OrderMutations, OrderQueries
from graphql_auth.schema import UserQuery, MeQuery

class Query(
    # AccountQueries,
    # CoreQueries,
    MeQuery,
    # OrderQueries,
    UserQuery,
):
    pass


class Mutation(
    AuthMutations,
    # AccountMutations,
    # CoreMutations,
    # OrderMutations,
):
    pass


schema = build_schema(query=Query, mutation=Mutation)
