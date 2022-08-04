"""Stream type classes for tap-anvil."""

from tap_anvil.client import AnvilStream


class WeldsStream(AnvilStream):
    """Define weld stream."""

    name = "welds"
    records_jsonpath = "$.data.currentUser.organizations[*].welds[*]"
    replication_key = None


# class GroupsStream(AnvilStream):
#     """Define custom stream."""
#
#     name = "groups"
#     schema = th.PropertiesList(
#         th.Property("name", th.StringType),
#         th.Property("id", th.StringType),
#         th.Property("modified", th.DateTimeType),
#     ).to_dict()
#     primary_keys = ["id"]
#     replication_key = "modified"
#     graphql_query = """
#         groups {
#             name
#             id
#             modified
#         }
#         """
