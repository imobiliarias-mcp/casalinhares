"""Builds Imobzi API search query parameters from domain filters."""

from scripts.domain.criteria import RentalFilter


class RentalQueryBuilder:
    """Translates high-level domain RentalFilter into HTTP query dictionary."""

    def _append_location(self, target_dictionary: dict, search_filter: RentalFilter) -> None:
        """Append city and neighborhood if specified."""
        city_name = search_filter.criteria.location.city
        if city_name:
            target_dictionary["city"] = city_name
        neighborhood_name = search_filter.criteria.location.neighborhood
        if neighborhood_name:
            target_dictionary["neighborhood"] = neighborhood_name

    def _append_specifications(self, target_dictionary: dict, search_filter: RentalFilter) -> None:
        """Append property type and bedroom thresholds."""
        type_name = search_filter.criteria.specifications.property_type
        if type_name:
            target_dictionary["property_type"] = type_name
        bedrooms = search_filter.criteria.specifications.minimum_bedrooms
        if bedrooms > 0:
            target_dictionary["bedroom_gte"] = str(bedrooms)

    def _append_price_range(self, target_dictionary: dict, search_filter: RentalFilter) -> None:
        """Append minimum and maximum price constraints."""
        price_range = search_filter.constraints.price_range
        min_amount = price_range.minimum_price.value()
        if min_amount > 0.0:
            target_dictionary["value_min"] = str(min_amount)
        max_amount = price_range.maximum_price.value()
        if max_amount > 0.0:
            target_dictionary["value_max"] = str(max_amount)

    def _append_pagination(self, target_dictionary: dict, search_filter: RentalFilter) -> None:
        """Append page number or cursor token."""
        cursor_token = search_filter.constraints.pagination.cursor_token
        if cursor_token:
            target_dictionary["cursor"] = cursor_token
            return
        page_index = search_filter.constraints.pagination.page_number
        target_dictionary["page"] = str(page_index)

    def build_parameters(self, search_filter: RentalFilter) -> dict[str, str]:
        """Convert a RentalFilter into full query parameter dictionary."""
        query_map: dict[str, str] = {
            "availability": "rent",
            "direction": "desc",
            "order": "created_at",
            "with_photos": "true",
            "with_listing_broker_count": "true",
        }
        self._append_location(query_map, search_filter)
        self._append_specifications(query_map, search_filter)
        self._append_price_range(query_map, search_filter)
        self._append_pagination(query_map, search_filter)
        return query_map
