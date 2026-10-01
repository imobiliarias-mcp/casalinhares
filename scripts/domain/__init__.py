"""Domain package for rental research."""

from scripts.domain.exceptions import (
    RentalSearchException,
    InvalidPriceException,
    InvalidPropertyCodeException,
    InvalidFilterException,
    PropertyNotFoundException,
    TenantResolutionException,
    ProviderTransportException,
)
from scripts.domain.value_objects import (
    ListingPrice,
    PropertyCode,
    GeoCoordinate,
)
from scripts.domain.criteria import (
    PriceRange,
    LocationCriteria,
    SpecificationCriteria,
    SearchPagination,
    RentalSearchCriteria,
    SearchConstraints,
    RentalFilter,
)
from scripts.domain.entities import (
    RentalListing,
    RentalPropertyDetail,
)
from scripts.domain.collections import (
    RentalListingCollection,
    FacetCollection,
    RentalSearchResult,
)

__all__ = [
    "RentalSearchException",
    "InvalidPriceException",
    "InvalidPropertyCodeException",
    "InvalidFilterException",
    "PropertyNotFoundException",
    "TenantResolutionException",
    "ProviderTransportException",
    "ListingPrice",
    "PropertyCode",
    "GeoCoordinate",
    "PriceRange",
    "LocationCriteria",
    "SpecificationCriteria",
    "SearchPagination",
    "RentalSearchCriteria",
    "SearchConstraints",
    "RentalFilter",
    "RentalListing",
    "RentalPropertyDetail",
    "RentalListingCollection",
    "FacetCollection",
    "RentalSearchResult",
]
