"""Parsers converting raw Imobzi JSON responses into domain entities."""

from scripts.domain.value_objects import ListingPrice, PropertyCode
from scripts.domain.entities import (
    ListingIdentity,
    ListingValuation,
    ListingCore,
    ListingDetails,
    RentalListing,
    DetailedProfile,
    RentalPropertyDetail,
)
from scripts.domain.collections import (
    RentalListingCollection,
    RentalSearchResult,
    FacetCollection,
)


class SearchResultParser:
    """Parses property search response payloads into RentalSearchResult."""

    def _build_core(self, item: dict) -> ListingCore:
        """Construct core identification and valuation."""
        code_vo = PropertyCode(str(item.get("code", "")))
        title_str = str(item.get("site_title", ""))
        identity = ListingIdentity(code=code_vo, title=title_str)
        price_amount = float(item.get("rental_value", 0.0) or 0.0)
        price_vo = ListingPrice(price_amount)
        property_type = str(item.get("property_type", "Imóvel"))
        valuation = ListingValuation(rental_price=price_vo, property_type=property_type)
        return ListingCore(identity=identity, valuation=valuation)

    def _build_details(self, item: dict) -> ListingDetails:
        """Construct location and media details."""
        neighborhood = str(item.get("neighborhood", ""))
        city = str(item.get("city", ""))
        location = f"{neighborhood}, {city}" if neighborhood and city else city
        cover_dict = item.get("cover_photo")
        cover_url = str(cover_dict.get("url", "")) if isinstance(cover_dict, dict) else ""
        return ListingDetails(location_summary=location, media_url=cover_url)

    def _extract_single_listing(self, item: dict) -> RentalListing:
        """Convert a raw property JSON object into a domain RentalListing."""
        core = self._build_core(item)
        details = self._build_details(item)
        return RentalListing(core=core, details=details)

    def _parse_items(self, raw_items: list) -> tuple[RentalListing, ...]:
        """Convert a list of raw dictionaries into listings tuple."""
        parsed = []
        for raw_item in raw_items:
            listing = self._extract_single_listing(raw_item)
            parsed.append(listing)
        return tuple(parsed)

    def parse_search_response(self, response_data: dict) -> RentalSearchResult:
        """Parse complete search response dictionary."""
        container = response_data.get("properties")
        if not isinstance(container, dict):
            return RentalSearchResult(collection=RentalListingCollection(()), total_listings_count=0)
        total_count = int(container.get("count", 0) or 0)
        raw_items = container.get("properties")
        if not isinstance(raw_items, list):
            return RentalSearchResult(collection=RentalListingCollection(()), total_listings_count=total_count)
        listings_tuple = self._parse_items(raw_items)
        collection = RentalListingCollection(listings=listings_tuple)
        return RentalSearchResult(collection=collection, total_listings_count=total_count)


class PropertyDetailParser:
    """Parses single property response into RentalPropertyDetail."""

    def _build_amenities(self, item: dict) -> str:
        """Format room counts and dimensions."""
        bedrooms = int(item.get("bedroom", 0) or 0)
        bathrooms = int(item.get("bathroom", 0) or 0)
        garages = int(item.get("garage", 0) or 0)
        area = float(item.get("area", 0.0) or item.get("useful_area", 0.0) or 0.0)
        return f"{bedrooms} quartos, {bathrooms} banheiros, {garages} vagas, {area} m²"

    def parse_detail_response(self, item: dict) -> RentalPropertyDetail:
        """Parse raw property detail JSON into RentalPropertyDetail entity."""
        search_parser = SearchResultParser()
        base_listing = search_parser._extract_single_listing(item)
        raw_desc = str(item.get("description", ""))
        desc = raw_desc if raw_desc else str(item.get("site_description", ""))
        amenities = self._build_amenities(item)
        profile = DetailedProfile(description=desc, amenities_summary=amenities)
        return RentalPropertyDetail(listing=base_listing, profile=profile)


class FacetParser:
    """Parses search fields facets response into FacetCollection."""

    def parse_facets_response(self, response_data: dict) -> FacetCollection:
        """Extract city and neighborhood facets from API response."""
        cities_raw = response_data.get("cities")
        cities_tuple = tuple(cities_raw) if isinstance(cities_raw, list) else ()
        neighborhoods_raw = response_data.get("neighborhoods")
        neighborhoods_tuple = tuple(neighborhoods_raw) if isinstance(neighborhoods_raw, list) else ()

        facet_map = {
            "cities": cities_tuple,
            "neighborhoods": neighborhoods_tuple,
        }
        return FacetCollection(facet_map=facet_map)
