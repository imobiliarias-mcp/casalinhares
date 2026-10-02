"""Domain package for rental research."""

from scripts.domain.collections import (
    FacetCollection,
    RentalListingCollection,
    RentalSearchResult,
)
from scripts.domain.criteria import (
    LocationCriteria,
    PriceRange,
    RentalFilter,
    RentalSearchCriteria,
    SearchConstraints,
    SearchPagination,
    SpecificationCriteria,
)
from scripts.domain.entities import (
    ListingDetails,
    ListingResources,
    RentalListing,
    RentalPropertyDetail,
)
from scripts.domain.exceptions import (
    InvalidFilterException,
    InvalidPriceException,
    InvalidPropertyCodeException,
    PropertyNotFoundException,
    ProviderTransportException,
    RentalSearchException,
    TenantResolutionException,
)
from scripts.domain.value_objects import (
    GeoCoordinate,
    ListingPrice,
    PropertyCode,
)

__all__ = [
    "FacetCollection",
    "GeoCoordinate",
    "InvalidFilterException",
    "InvalidPriceException",
    "InvalidPropertyCodeException",
    "ListingDetails",
    "ListingPrice",
    "ListingResources",
    "LocationCriteria",
    "PriceRange",
    "PropertyCode",
    "PropertyNotFoundException",
    "ProviderTransportException",
    "RentalFilter",
    "RentalListing",
    "RentalListingCollection",
    "RentalPropertyDetail",
    "RentalSearchCriteria",
    "RentalSearchException",
    "RentalSearchResult",
    "SearchConstraints",
    "SearchPagination",
    "SpecificationCriteria",
    "TenantResolutionException",
]
