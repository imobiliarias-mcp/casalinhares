# Central Rental Research MCP — Casa Linhares Module

This package implements the **Casa Linhares** rental search provider designed as a plug-and-play adapter for a **Central Rental Research MCP (Model Context Protocol)** server.

---

## 1. Architectural Highlights

- **SOLID Principles**: Single responsibility classes, interface segregation, dependency inversion.
- **Strict Object Calisthenics**:
  - One indent level per method.
  - Zero `else` keywords (guard clauses and polymorphism only).
  - Wrapped primitives (Value Objects for prices, coordinates, filters).
  - First-class collections (`RentalListingCollection`, `PhotoCollection`, `FacetCollection`).
  - One dot per line (intermediate assigned variables).
  - No abbreviations.
  - Entities size limits: functions ≤ 15 lines, classes ≤ 100 lines, modules < 200 lines.
  - ≤ 2 instance variables per class.
  - Tell, Don't Ask encapsulation.
- **Design Patterns**: Adapter, Strategy, Builder, Value Object, First-Class Collection, Factory.
- **Fail Fast**: Immediate boundary validation on inputs, raising descriptive typed domain exceptions.

---

## 2. Directory Layout

```
scripts/
├── README.md               # Package overview and developer instructions
├── ARCHITECTURE.md         # Calisthenics & SOLID design adherence documentation
├── USAGE.md                # Usage examples and MCP integration guide
├── __init__.py
├── domain/                 # Pure domain layer
│   ├── __init__.py
│   ├── exceptions.py       # Domain exception hierarchy
│   ├── value_objects.py    # Immutable value objects (Price, Filter, Coordinates)
│   ├── entities.py         # Domain models (RentalListing, PropertyDetail)
│   └── collections.py      # First-class collections (RentalListingCollection, etc.)
├── interfaces/             # Port contracts (MCP Provider Protocols)
│   ├── __init__.py
│   └── provider.py         # RentalProviderProtocol interface
├── client/                 # Infrastructure & Imobzi HTTP client
│   ├── __init__.py
│   ├── configuration.py    # Imobzi client configuration
│   ├── resolver.py         # Dynamic tenant database resolver
│   ├── http_transport.py   # Origin-aware HTTP transport
│   ├── query_builder.py    # Filter-to-query translator
│   └── parsers.py          # Response parsers
├── providers/              # Adapter layer
│   ├── __init__.py
│   └── casalinhares.py     # CasaLinharesRentalProvider implementation
├── mcp/                    # MCP tool contracts & handlers
│   ├── __init__.py
│   └── tools.py            # Central Rental Research MCP tools
├── run_search.py           # CLI tool to run rental searches
├── run_property_detail.py  # CLI tool to fetch full property details
├── run_facets.py           # CLI tool to list search facets
└── run_tests.py            # Full test suite runner
```

---

## 3. Running the CLI Tools

### Search Rentals
```bash
# Basic rental search (defaults to Timóteo & Ipatinga)
python3 scripts/run_search.py

# Filter by city, bedrooms, and maximum price
python3 scripts/run_search.py --city Timóteo --bedrooms 2 --max-price 3000
```

### Get Property Details
```bash
# Fetch complete detail for property code 1443
python3 scripts/run_property_detail.py 1443
```

### Inspect Search Facets
```bash
# Retrieve available cities, neighborhoods, and price ranges
python3 scripts/run_facets.py
```

### Run Automated Tests
```bash
# Execute unit and integration tests
python3 scripts/run_tests.py
```
