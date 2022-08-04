"""Stream type classes for tap-anvil."""

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_anvil.client import AnvilStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class UsersStream(AnvilStream):
    """Define custom stream."""

    name = "users"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property("id", th.StringType, description="The user's system ID"),
        th.Property(
            "address",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("city", th.StringType),
                th.Property(
                    "state",
                    th.StringType,
                    description="State name in ISO 3166-2 format",
                ),
                th.Property("zip", th.StringType),
            ),
        ),
    ).to_dict()
    primary_keys = ["id"]
    replication_key = None
    graphql_query = """
        users {
            name
            id
            age
            email
            address {
                street
                city
                state
                zip
            }
        }
        """


class GroupsStream(AnvilStream):
    """Define custom stream."""

    name = "groups"
    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property("id", th.StringType),
        th.Property("modified", th.DateTimeType),
    ).to_dict()
    primary_keys = ["id"]
    replication_key = "modified"
    graphql_query = """
        groups {
            name
            id
            modified
        }
        """
