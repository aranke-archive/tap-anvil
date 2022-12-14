"""Stream type classes for tap-anvil."""
from typing import Any, Dict, Optional

import requests

from tap_anvil.client import AnvilStream


class OrganizationsStream(AnvilStream):
    """Define organization stream."""

    name = "organizations"
    jsonpath = "$.data.currentUser.organizations[*]"
    records_jsonpath: Any = jsonpath

    def get_child_context(
        self, record: Dict[str, Any], context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Pass organization slug to child weld."""
        return {
            "slug": record["slug"],
        }


class WeldsStream(AnvilStream):
    """Define weld stream."""

    name = "welds"
    parent_stream_type = OrganizationsStream
    jsonpath = "$.data.organization.welds[*]"
    records_jsonpath: Any = jsonpath
    ignore_parent_replication_keys = True

    def prepare_request_payload(
        self, context: Optional[Dict[str, Any]], next_page_token: Optional[int]
    ) -> Dict[str, Any]:
        """Inject GraphQL variables into payload."""
        assert context is not None
        slug = context["slug"]

        return {
            "query": self.query,
            "variables": {"slug": slug},
        }

    def get_child_context(
        self, record: Dict[str, Any], context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Pass weld EID to child weld data."""
        return {
            "eid": record["eid"],
        }

    def post_process(
        self, row: Dict[str, Any], context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add organization information to record."""
        assert context is not None
        row["organizationSlug"] = context["slug"]
        return row


class ForgesStream(AnvilStream):
    """Define forge stream."""

    name = "forges"
    parent_stream_type = WeldsStream
    jsonpath = "$.data.weld.forges[*]"
    records_jsonpath: Any = jsonpath
    ignore_parent_replication_keys = True

    def prepare_request_payload(
        self, context: Optional[Dict[str, Any]], next_page_token: Optional[int]
    ) -> Dict[str, Any]:
        """Inject GraphQL variables into payload."""
        assert context is not None
        eid = context["eid"]

        return {
            "query": self.query,
            "variables": {"eid": eid},
        }

    def post_process(
        self, row: Dict[str, Any], context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add weld information to record."""
        assert context is not None
        row["weldEid"] = context["eid"]
        return row


class WeldDatasStream(AnvilStream):
    """Define weld data stream."""

    name = "weldDatas"
    parent_stream_type = WeldsStream
    jsonpath = "$.data.weld.weldDatas.items[*]"
    records_jsonpath: Any = jsonpath
    ignore_parent_replication_keys = True

    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: Optional[int],
    ) -> Optional[int]:
        """Handle pagination."""
        data = response.json()
        page = data["data"]["weld"]["weldDatas"]

        if data:
            page_index = int(page["page"])
            page_count = int(page["pageCount"])
            page_size = int(page["pageSize"])
            if page_index < page_count:
                return page_index + page_size

        return None

    def prepare_request_payload(
        self, context: Optional[Dict[str, Any]], next_page_token: Optional[int]
    ) -> Dict[str, Any]:
        """Inject GraphQL variables into payload."""
        offset = next_page_token or 1
        assert context is not None
        eid = context["eid"]

        return {
            "query": self.query,
            "variables": {"eid": eid, "offset": offset},
        }

    def get_child_context(
        self, record: Dict[str, Any], context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Pass weld EID to child weld data."""
        return {
            "eid": record["eid"],
        }

    def post_process(
        self, row: Dict[str, Any], context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add weld information to record."""
        assert context is not None
        row["weldEid"] = context["eid"]
        return row


class SubmissionsStream(AnvilStream):
    """Define submission stream."""

    name = "submissions"
    parent_stream_type = WeldDatasStream
    jsonpath = "$.data.weldData.submissions[*]"
    records_jsonpath: Any = jsonpath
    ignore_parent_replication_keys = True

    def prepare_request_payload(
        self, context: Optional[Dict[str, Any]], next_page_token: Optional[int]
    ) -> Dict[str, Any]:
        """Inject GraphQL variables into payload."""
        assert context is not None
        eid = context["eid"]

        return {
            "query": self.query,
            "variables": {"eid": eid},
        }

    def post_process(
        self, row: Dict[str, Any], context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add weld information to record."""
        assert context is not None
        row["weldDataEid"] = context["eid"]
        return row
