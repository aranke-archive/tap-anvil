"""Stream type classes for tap-anvil."""
from typing import Optional

import requests  # type: ignore

from tap_anvil.client import AnvilStream


class WeldsStream(AnvilStream):
    """Define weld stream."""

    name = "welds"
    primary_keys = ["eid"]

    jsonpath = "$.data.currentUser.organizations[*].welds[*]"
    records_jsonpath = jsonpath  # type: ignore
    replication_key = "updatedAt"

    def get_child_context(self, record: dict, context: dict) -> dict:
        """Pass weld EID to child weld data."""
        return {
            "eid": record["eid"],
        }


class WeldDatasStream(AnvilStream):
    """Define weld data stream."""

    name = "weldDatas"
    primary_keys = ["eid"]
    parent_stream_type = WeldsStream

    jsonpath = "$.data.weld.weldDatas.items[*]"
    records_jsonpath = jsonpath  # type: ignore

    ignore_parent_replication_keys = True
    replication_key = "updatedAt"

    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: int,
    ) -> int:
        """Handle pagination."""
        data = response.json()
        page = data["data"]["weld"]["weldDatas"]

        if data:
            page_index = page["page"]
            page_count = page["pageCount"]
            page_size = page["pageSize"]
            if page_index < page_count:
                return page_index + page_size

        return None

    def prepare_request_payload(self, context: dict, next_page_token: int) -> dict:
        """Inject GraphQL variables into payload."""
        return {
            "query": self.query,
            "variables": {"eid": context["eid"], "offset": next_page_token},
        }

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """Add weld information to record."""
        for k in ["eid", "slug", "name"]:
            row["weld" + k.title()] = row["weld"][k]
        del row["weld"]
        return row
