"""Domain exceptions for rental research."""


class RentalSearchException(Exception):
    """Base domain exception for rental research operations."""


class InvalidPropertyCodeException(RentalSearchException):
    """Raised when a property listing code is malformed or empty."""


class InvalidPriceException(RentalSearchException):
    """Raised when a listing price is invalid or negative."""


class InvalidFilterException(RentalSearchException):
    """Raised when search filter criteria violate business invariants."""


class PropertyNotFoundException(RentalSearchException):
    """Raised when a requested property listing is not found."""


class TenantResolutionException(RentalSearchException):
    """Raised when resolving a tenant hostname to database identifier fails."""


class ProviderTransportException(RentalSearchException):
    """Raised when low-level HTTP transport communication fails."""
