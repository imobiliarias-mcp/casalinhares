"""Casa Linhares rental search provider implementation."""

import httpx
from scripts.client.configuration import ImobziConfiguration
from scripts.client.http_transport import ImobziHttpTransport
from scripts.client.resolver import TenantDatabaseResolver
from scripts.client.query_builder import RentalQueryBuilder
from scripts.client.parsers import (
    SearchResultParser,
    PropertyDetailParser,
    FacetParser,
)
from scripts.domain.criteria import RentalFilter
from scripts.domain.value_objects import PropertyCode
from scripts.domain.entities import RentalPropertyDetail
from scripts.domain.collections import (
    RentalSearchResult,
    FacetCollection,
)
from scripts.interfaces.provider import RentalProviderProtocol


class CasaLinharesRentalProvider(RentalProviderProtocol):
    """Adapter implementing RentalProviderProtocol for Casa Linhares portal."""

    def __init__(
        self,
        transport: ImobziHttpTransport,
        resolver: TenantDatabaseResolver,
    ) -> None:
        """Initialize provider with transport and tenant resolver."""
        self._transport = transport
        self._resolver = resolver

    @classmethod
    def create_default(cls) -> "CasaLinharesRentalProvider":
        """Factory method constructing provider with default configurations."""
        configuration = ImobziConfiguration()
        client = httpx.Client(timeout=15.0)
        transport = ImobziHttpTransport(configuration=configuration, http_client=client)
        resolver = TenantDatabaseResolver(transport=transport, configuration=configuration)
        return cls(transport=transport, resolver=resolver)

    def provider_name(self) -> str:
        """Return unique provider identifier for central MCP registry."""
        return "casa_linhares"

    def search_rentals(self, search_filter: RentalFilter) -> RentalSearchResult:
        """Search rental listings using criteria."""
        database_id = self._resolver.resolve_database_identifier()
        endpoint_url = f"https://api2.imobzi.app/v1/{database_id}/site2/search/properties"
        query_builder = RentalQueryBuilder()
        query_parameters = query_builder.build_parameters(search_filter)
        raw_response = self._transport.get_json(endpoint_url, query_parameters)
        parser = SearchResultParser()
        return parser.parse_search_response(raw_response)

    def get_property_detail(self, code: PropertyCode) -> RentalPropertyDetail:
        """Retrieve full details for a single property by code."""
        database_id = self._resolver.resolve_database_identifier()
        code_string = code.value()
        endpoint_url = f"https://api2.imobzi.app/v1/{database_id}/site2/properties/{code_string}"
        parameters = {"listing_broker_properties_count": "true"}
        raw_response = self._transport.get_json(endpoint_url, parameters)
        parser = PropertyDetailParser()
        return parser.parse_detail_response(raw_response)

    def get_facets(self) -> FacetCollection:
        """Retrieve available cities, neighborhoods, and filter options."""
        database_id = self._resolver.resolve_database_identifier()
        endpoint_url = f"https://api2.imobzi.app/v1/{database_id}/site2/properties/search/fields"
        parameters = {
            "availability": "rent",
            "all_fields": "true",
            "filters_show_total": "true",
            "search_type": "filter_without_count",
        }
        raw_response = self._transport.get_json(endpoint_url, parameters)
        parser = FacetParser()
        return parser.parse_facets_response(raw_response)
