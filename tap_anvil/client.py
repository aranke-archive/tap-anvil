"""GraphQL client handling, including anvilStream base class."""

from typing import Iterable

import requests
from singer_sdk.streams import GraphQLStream


class AnvilStream(GraphQLStream):
    """anvil stream class."""

    # TODO: Set the API's base URL here:
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    # Alternatively, use a static string for url_base:
    # url_base = "https://api.mysample.com"

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # headers["Private-Token"] = self.config.get("auth_token")
        return headers

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records.
        resp_json = response.json()
        for row in resp_json.get("<TODO>"):
            yield row
