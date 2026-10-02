# Central Rental Research MCP — Usage Guide

This guide illustrates how to use the Casa Linhares rental search module both as a standalone library and as an MCP (Model Context Protocol) tool provider.

---

## 1. Python API Usage

### 1.1 Basic Search
```python
from scripts.providers.casalinhares import CasaLinharesRentalProvider
from scripts.domain.value_objects import RentalFilter, ListingPrice

provider = CasaLinharesRentalProvider.create_default()

# Search all rentals
search_result = provider.search_rentals(RentalFilter())
print(f"Total found: {search_result.total_count()}")

for listing in search_result.listings():
    print(listing.format_summary())
    print("Public property URL:", listing.to_dictionary()["url"])
```

### 1.2 Filtered Search
```python
from scripts.domain.value_objects import RentalFilter, ListingPrice

# Search 2+ bedroom rentals in Timóteo under R$ 3,000/month
criteria = (
    RentalFilter()
    .with_city("Timóteo")
    .with_minimum_bedrooms(2)
    .with_maximum_price(ListingPrice(3000.0))
)

result = provider.search_rentals(criteria)
for item in result.listings():
    print(item.format_summary())
```

### 1.3 Fetch Property Details
```python
from scripts.domain.value_objects import PropertyCode

code = PropertyCode("1443")
detail = provider.get_property_detail(code)
print(detail.format_detailed_view())
```

### 1.4 Inspect Available Facets (Neighborhoods & Price Ranges)
```python
facets = provider.get_facets()
print("Cities:", facets.city_names())
print("Neighborhoods:", facets.neighborhood_names())
print("Price range:", facets.price_range_summary())
```

---

## 2. Integrating with a Central Rental Research MCP Server

If you are running an MCP server (e.g. using `FastMCP` or standard MCP SDK):

```python
from mcp.server.fastmcp import FastMCP
from scripts.mcp.tools import CasaLinharesMcpAdapter

mcp = FastMCP("Central Rental Research MCP")
adapter = CasaLinharesMcpAdapter.create_default()

@mcp.tool()
def search_rentals_casalinhares(
    city: str = "",
    min_price: float = 0.0,
    max_price: float = 0.0,
    bedrooms: int = 0,
    property_type: str = "",
    page: int = 1,
) -> dict:
    """Search rental listings from Casa Linhares in Vale do Aço (Timóteo, Ipatinga)."""
    return adapter.search_rentals(
        city=city,
        min_price=min_price,
        max_price=max_price,
        bedrooms=bedrooms,
        property_type=property_type,
        page=page,
    )

@mcp.tool()
def get_rental_property_detail(property_code: str) -> dict:
    """Get full details, photos, and broker contacts for a specific Casa Linhares property."""
    return adapter.get_property_detail(property_code)

@mcp.tool()
def get_rental_search_facets() -> dict:
    """List available cities, neighborhoods, and price ranges for rental properties."""
    return adapter.get_facets()

if __name__ == "__main__":
    mcp.run()
```

---

## 3. CLI Utilities Reference

| Command | Purpose | Example |
|:---|:---|:---|
| `python3 scripts/run_search.py` | Run parameterized rental searches | `python3 scripts/run_search.py --city Ipatinga --min-price 1000` |
| `python3 scripts/run_property_detail.py <CODE>` | View complete details of a listing | `python3 scripts/run_property_detail.py 1443` |
| `python3 scripts/run_facets.py` | View cities, neighborhoods & prices | `python3 scripts/run_facets.py` |
| `python3 scripts/run_tests.py` | Run test suite | `python3 scripts/run_tests.py` |
