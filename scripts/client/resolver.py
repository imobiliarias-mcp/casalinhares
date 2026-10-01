"""Tenant database namespace resolver."""

from scripts.client.configuration import ImobziConfiguration
from scripts.client.http_transport import ImobziHttpTransport
from scripts.domain.exceptions import TenantResolutionException


class TenantDatabaseResolver:
    """Discovers and caches the internal database namespace for an Imobzi website."""

    def __init__(
        self,
        transport: ImobziHttpTransport,
        configuration: ImobziConfiguration,
    ) -> None:
        """Initialize resolver with transport and configuration."""
        self._transport = transport
        self._configuration = configuration
        self._cached_database_identifier: str = ""

    def _build_lookup_url(self) -> str:
        """Build database discovery URL for configured host."""
        api_root = self._configuration.api_base_url
        hostname = self._configuration.base_hostname
        return f"{api_root}/site/database/{hostname}"

    def _extract_database_field(self, payload: dict) -> str:
        """Extract database namespace string from JSON response."""
        database_value = payload.get("database")
        if not database_value:
            raise TenantResolutionException("Response missing 'database' namespace key.")
        return str(database_value)

    def resolve_database_identifier(self) -> str:
        """Resolve and cache tenant database namespace."""
        if self._cached_database_identifier:
            return self._cached_database_identifier
        lookup_url = self._build_lookup_url()
        response_data = self._transport.get_json(lookup_url)
        if not isinstance(response_data, dict):
            raise TenantResolutionException("Expected JSON object from database discovery.")
        identifier = self._extract_database_field(response_data)
        self._cached_database_identifier = identifier
        return identifier
