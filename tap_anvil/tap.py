"""anvil tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_anvil.streams import GroupsStream, UsersStream

STREAM_TYPES = [
    UsersStream,
    GroupsStream,
]


class TapAnvil(Tap):
    """anvil tap class."""

    name = "tap-anvil"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "project_ids",
            th.ArrayType(th.StringType),
            required=True,
            description="Project IDs to replicate",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.mysample.com",
            description="The url for the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
