"""Offline public property URL contract tests for Casa Linhares."""

import pytest

from scripts.client.configuration import ImobziConfiguration
from scripts.client.parsers import PropertyDetailParser, SearchResultParser
from scripts.domain.criteria import RentalFilter
from scripts.domain.entities import (
    ListingCore,
    ListingDetails,
    ListingIdentity,
    ListingResources,
    ListingValuation,
    RentalListing,
)
from scripts.domain.value_objects import ListingPrice, PropertyCode
from scripts.mcp.tools import CasaLinharesMcpAdapter
from scripts.providers.casalinhares import CasaLinharesRentalProvider
from scripts.run_search import display_results

PUBLIC_BASE = "https://www.casalinhares.com.br"
CUSTOM_BASE = "https://listings.example.test"


@pytest.mark.parametrize(
    ("details", "expected_media_url"),
    [
        (ListingDetails("Eldorado, Timóteo", media_url="keyword.jpg"), "keyword.jpg"),
        (ListingDetails("Eldorado, Timóteo", "positional.jpg"), "positional.jpg"),
        (
            ListingDetails(
                "Eldorado, Timóteo",
                resources=ListingResources(media_url="composed.jpg", property_url="https://example.test/property"),
            ),
            "composed.jpg",
        ),
    ],
    ids=("legacy-keyword", "legacy-positional", "composed-resources"),
)
def test_listing_details_exposes_legacy_media_url(details, expected_media_url: str) -> None:
    """Expose media URL through both legacy and composed details construction."""
    assert details.media_url == expected_media_url


def payload_with_url(site_url: str | None = "/imovel/apartamento-eldorado-code-1427") -> dict:
    """Create the documented Imobzi search result shape."""
    property_data = {
        "code": "1427",
        "site_title": "Apartamento",
        "rental_value": 1500,
        "neighborhood": "Eldorado",
        "city": "Timóteo",
        "cover_photo": {"url": "https://media.imobzi.com/cover.jpg"},
    }
    if site_url is not None:
        property_data["site_url"] = site_url
    return {"properties": {"count": 1, "properties": [property_data]}}


def test_existing_search_parser_is_missing_public_url() -> None:
    """Expose the current missing-link regression through the existing parser API."""
    result = SearchResultParser().parse_search_response(payload_with_url())

    assert result.to_dictionary()["listings"][0]["url"] == (
        f"{PUBLIC_BASE}/imovel/apartamento-eldorado-code-1427"
    )


@pytest.mark.parametrize(
    ("site_url", "expected_url"),
    [
        (
            "https://www.casalinhares.com.br/imovel/apartamento-eldorado-code-1427",
            "https://www.casalinhares.com.br/imovel/apartamento-eldorado-code-1427",
        ),
        (
            "/imovel/apartamento-eldorado-code-1427?property_id=608",
            "https://www.casalinhares.com.br/imovel/apartamento-eldorado-code-1427?property_id=608",
        ),
        (
            "imovel/apartamento-eldorado-code-1427",
            "https://www.casalinhares.com.br/imovel/apartamento-eldorado-code-1427",
        ),
        (
            "//www.casalinhares.com.br/imovel/apartamento-eldorado-code-1427",
            "https://www.casalinhares.com.br/imovel/apartamento-eldorado-code-1427",
        ),
        (
            "/imovel/apartamento-eldorado?id=608",
            "https://www.casalinhares.com.br/imovel/apartamento-eldorado?id=608",
        ),
    ],
)
def test_search_parser_resolves_site_url_and_preserves_listing_fields(site_url: str, expected_url: str) -> None:
    """Normalize API-provided public URLs without changing legacy listing data."""
    result = SearchResultParser(public_base_url=PUBLIC_BASE).parse_search_response(payload_with_url(site_url))
    serialized = result.to_dictionary()
    listing = serialized["listings"][0]

    assert listing["url"] == expected_url
    assert listing["code"] == "1427"
    assert listing["rental_price"] == 1500.0
    assert listing["location"] == "Eldorado, Timóteo"
    assert listing["media_url"] == "https://media.imobzi.com/cover.jpg"
    assert serialized["returned_count"] == 1


def test_search_parser_rejects_missing_or_invalid_site_url_without_documented_fallback() -> None:
    """Fail with property context instead of fabricating a code-based route."""
    parser = SearchResultParser(public_base_url=PUBLIC_BASE)

    invalid_urls = (
        "javascript:alert(1)",
        "https://api2.imobzi.app/v1/database/site2/properties/1427",
        "https://media.imobzi.com/cover.jpg",
        "https://www.casalinhares.com.br/",
    )
    with pytest.raises(ValueError, match="1427"):
        parser.parse_search_response(payload_with_url(None))
    for invalid_url in invalid_urls:
        with pytest.raises(ValueError, match="1427"):
            parser.parse_search_response(payload_with_url(invalid_url))


@pytest.mark.parametrize("property_url", ["", "/imovel/apartamento/1427", "ftp://example.test/imovel/1427"])
def test_manual_listing_serializer_rejects_unresolved_public_url(property_url: str) -> None:
    """Keep the legacy listing constructor but reject missing/relative URLs."""
    detail_fields = {"location_summary": "Eldorado, Timóteo", "media_url": "legacy-image.jpg"}
    if property_url:
        detail_fields["property_url"] = property_url
    details = ListingDetails(**detail_fields)
    listing = RentalListing(
        core=ListingCore(
            identity=ListingIdentity(code=PropertyCode("1427"), title="Apartamento"),
            valuation=ListingValuation(rental_price=ListingPrice(1500), property_type="Apartamento"),
        ),
        details=details,
    )

    with pytest.raises(ValueError, match="1427"):
        listing.to_dictionary()


def test_provider_uses_configured_public_base_and_makes_no_detail_request() -> None:
    """Resolve URLs from tenant configuration while retaining one search call."""
    configuration = ImobziConfiguration(base_hostname="listings.example.test")
    transport = StubImobziTransport(configuration.public_base_url(), payload_with_url())
    provider = CasaLinharesRentalProvider(transport=transport, resolver=StubTenantResolver())

    result = provider.search_rentals(RentalFilter())

    assert result.to_dictionary()["listings"][0]["url"] == f"{CUSTOM_BASE}/imovel/apartamento-eldorado-code-1427"
    assert transport.call_count == 1


def test_property_detail_parser_keeps_public_url_in_detail_serialization() -> None:
    """Use the same boundary URL resolution for property-detail serialization."""
    detail_data = payload_with_url()["properties"]["properties"][0]
    detail_data["description"] = "Apartamento amplo"

    detail = PropertyDetailParser(public_base_url=PUBLIC_BASE).parse_detail_response(detail_data)

    assert detail.to_dictionary()["url"] == f"{PUBLIC_BASE}/imovel/apartamento-eldorado-code-1427"
    assert detail.to_dictionary()["amenities"]


def test_existing_mcp_adapter_and_cli_expose_the_public_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Expose one normalized URL through MCP JSON and the search CLI."""
    result = SearchResultParser(public_base_url=PUBLIC_BASE).parse_search_response(payload_with_url())
    adapter = CasaLinharesMcpAdapter(FixedSearchProvider(result))

    mcp_result = adapter.search_rentals(city="Timóteo")
    display_results(result)

    expected_url = f"{PUBLIC_BASE}/imovel/apartamento-eldorado-code-1427"
    assert mcp_result["listings"][0]["url"] == expected_url
    assert f"Link: {expected_url}" in capsys.readouterr().out


class StubTenantResolver:
    """Return a fixed Imobzi database namespace without network access."""

    def resolve_database_identifier(self) -> str:
        return "test-database"


class StubImobziTransport:
    """Serve the original search response and report configured public origin."""

    def __init__(self, public_base_url: str, json_data: dict) -> None:
        self._public_base_url = public_base_url
        self._json_data = json_data
        self.call_count = 0

    def public_base_url(self) -> str:
        return self._public_base_url

    def get_json(self, url: str, parameters: dict | None = None) -> dict:
        self.call_count += 1
        return self._json_data


class FixedSearchProvider:
    """Return a parsed search result from an injected provider boundary."""

    def __init__(self, result) -> None:
        self._result = result

    def search_rentals(self, _search_filter):
        return self._result
