"""Stream type classes for tap-anvil."""
from typing import Optional

import requests  # type: ignore

from tap_anvil.client import AnvilStream


class OrganizationsStream(AnvilStream):
    """Define organization stream."""

    name = 'organizations'
    primary_keys = ["eid"]

    jsonpath = "$.data.currentUser.organizations[*]"
    records_jsonpath = jsonpath  # type: ignore

    replication_key = "updatedAt"

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Pass organization slug to child weld."""
        return {
            "slug": record["slug"],
        }


class WeldsStream(AnvilStream):
    """Define weld stream."""

    name = "welds"
    primary_keys = ["eid"]
    parent_stream_type = OrganizationsStream

    jsonpath = "$.data.organization.welds[*]"
    records_jsonpath = jsonpath  # type: ignore

    ignore_parent_replication_keys = True
    replication_key = "updatedAt"

    def prepare_request_payload(
            self, context: Optional[dict], next_page_token: Optional[int]
    ) -> dict:
        """Inject GraphQL variables into payload."""
        slug = context.get("slug") if context else None

        return {
            "query": self.query,
            "variables": {"slug": slug},
        }

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Pass weld EID to child weld data."""
        return {
            "eid": record["eid"],
        }

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """Add organization information to record."""
        row["organizationSlug"] = context.get("slug") if context else None
        return row


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
            previous_token: Optional[int],
    ) -> Optional[int]:
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

    def prepare_request_payload(
            self, context: Optional[dict], next_page_token: Optional[int]
    ) -> dict:
        """Inject GraphQL variables into payload."""
        offset = next_page_token if next_page_token else 1
        eid = context.get("eid") if context else None

        return {
            "query": self.query,
            "variables": {"eid": eid, "offset": offset},
        }

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """Add weld information to record."""
        for k in ["eid", "slug", "name"]:
            row["weld" + k.title()] = row["weld"][k]
        del row["weld"]
        return row
