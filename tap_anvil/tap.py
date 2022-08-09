"""anvil tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_anvil.streams import WeldDatasStream, WeldsStream, OrganizationsStream

STREAM_TYPES = [OrganizationsStream, WeldsStream, WeldDatasStream]


class TapAnvil(Tap):
    """anvil tap class."""

    name = "tap-anvil"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="The API key to use to authenticate against Anvil",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
