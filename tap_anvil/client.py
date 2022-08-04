"""GraphQL client handling, including anvilStream base class."""
from pathlib import Path
from typing import Optional

from singer_sdk.authenticators import BasicAuthenticator
from singer_sdk.streams import GraphQLStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
QUERIES_DIR = Path(__file__).parent / Path("./queries")


class AnvilStream(GraphQLStream):
    """anvil stream class."""

    url_base = "https://graphql.useanvil.com"
    primary_keys = ["eid"]

    @property
    def schema_filepath(self) -> Optional[Path]:
        """Get the path to the schema file."""
        return SCHEMAS_DIR / Path(f"{self.name}.json")

    @property
    def query(self) -> str:
        """Get the query string."""
        qf = QUERIES_DIR / f"{self.name}.graphql"
        qs = qf.read_text()
        return qs

    @property
    def authenticator(self) -> BasicAuthenticator:
        """Return the authenticator."""
        return BasicAuthenticator.create_for_stream(
            self,
            username=self.config["api_key"],
            password="",
        )
