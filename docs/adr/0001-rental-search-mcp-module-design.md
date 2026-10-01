# ADR 0001: Architecture & Design of Central Rental Research MCP Modules

## Status
Accepted

## Context

The system requires reverse-engineering the rental property search API of **Casa Linhares** (`https://www.casalinhares.com.br/`) and architecting modular Python components intended for integration into a **Central Rental Research MCP (Model Context Protocol)** server.

A central MCP server allows AI assistants and client applications to query multiple real estate platforms (e.g. Casa Linhares, Netimóveis, QuintoAndar, Zap Imóveis) through a unified tool contract. To achieve this, the integration must not be a monolithic scraping script, but rather a decoupled, highly cohesive, modular architecture.

Furthermore, the implementation must strictly satisfy:
- **SOLID Principles**
- **Clean Code**
- **Object Calisthenics** (9 strict rules)
- **Design Patterns** (Adapter, Strategy, Value Object, First-Class Collection, Factory)
- **Fail-Fast input validation**
- **Defensive error handling**

---

## Decision

We adopt a **Hexagonal / Ports-and-Adapters Architecture** partitioned into four explicit layers:

```
┌────────────────────────────────────────────────────────┐
│               Central Rental Research MCP              │
│               (Model Context Protocol Tools)           │
└──────────────────────────┬─────────────────────────────┘
                           │ uses Port (Protocol)
                           ▼
┌────────────────────────────────────────────────────────┐
│                   Domain Layer                         │
│  - Value Objects (Price, Coordinates, Filter, Codes)   │
│  - First-Class Collections (Listings, Photos, Facets)  │
│  - Domain Exceptions                                   │
│  - Provider Port Interface (RentalProviderProtocol)    │
└──────────────────────────▲─────────────────────────────┘
                           │ implements Port
┌──────────────────────────┴─────────────────────────────┐
│                 Adapter / Provider Layer               │
│  - CasaLinharesRentalProvider                          │
│  - Adapts Imobzi API responses to Domain Entities      │
└──────────────────────────┬─────────────────────────────┘
                           │ coordinates
┌──────────────────────────▼─────────────────────────────┐
│                  Infrastructure Layer                  │
│  - TenantDatabaseResolver (Dynamic namespace lookup)   │
│  - ImobziHttpTransport (Origin/Referer headers)        │
│  - RentalQueryBuilder (Translates filter to Imobzi API)│
│  - Parsers (SearchResultParser, DetailParser, etc.)    │
└────────────────────────────────────────────────────────┘
```

---

## Object Calisthenics Enforcement Matrix

| Calisthenics Rule | Implementation Strategy in Python |
|:---|:---|
| **1. One level of indentation per method** | Deep loops and branching are decomposed into named single-purpose private helper methods. |
| **2. Don't use the `else` keyword** | Guard clauses, early returns, polymorphic strategies, or dictionary dispatch tables are used exclusively. |
| **3. Wrap all primitives and strings** | Raw primitives are wrapped in domain value objects: `ListingPrice`, `PropertyCode`, `GeoCoordinate`, `RentalFilter`, `PaginationToken`. |
| **4. First-class collections** | Any class containing a collection contains no other member fields, exposing only domain collection operations: `RentalListingCollection`, `PhotoCollection`, `FacetCollection`. |
| **5. One dot per line** | No deep chaining (`a.b().c()`). Every intermediate object is assigned to an explicitly named local variable. |
| **6. Don't abbreviate** | Descriptive domain naming throughout (`response`, `request`, `listing`, `property_entity`, `database_identifier`, `broker_portfolio`). |
| **7. Keep all entities small** | Functions ≤ 15 lines, classes ≤ 100 lines, modules ≤ 200 lines. |
| **8. No classes with more than 2 instance variables** | Classes hold at most 2 member fields. Larger state is factored into value objects or collaborator objects. |
| **9. No getters/setters (Tell, Don't Ask)** | Domain objects encapsulate their state and expose behaviors or representations (`to_dict`, `matches_price_ceiling`, `format_display`), not mutable getters/setters. |

---

## SOLID Principles Application

### Single Responsibility Principle (SRP)
- `ImobziHttpTransport`: Strictly responsible for low-level HTTP transport and headers.
- `TenantDatabaseResolver`: Strictly responsible for resolving a domain hostname to an Imobzi tenant namespace.
- `RentalQueryBuilder`: Strictly responsible for converting high-level `RentalFilter` to URL query parameters.
- `SearchResultParser`: Strictly responsible for validating and parsing raw JSON into `RentalListingCollection`.
- `CasaLinharesRentalProvider`: Strictly responsible for orchestrating the client components to fulfill the `RentalProviderProtocol`.

### Open/Closed Principle (OCP)
The central MCP server interacts exclusively with `RentalProviderProtocol`. New real estate platforms (e.g. Netimóveis, QuintoAndar) can be added as new providers without modifying existing tool handlers.

### Liskov Substitution Principle (LSP)
`CasaLinharesRentalProvider` satisfies all invariants of `RentalProviderProtocol`. Substituting it with any other provider yields predictable, equivalent behavioral contracts.

### Interface Segregation Principle (ISP)
The provider capabilities are split into focused sub-protocols:
- `RentalSearchCapability` (`search_rentals`)
- `RentalDetailCapability` (`get_property_detail`)
- `RentalFacetsCapability` (`get_facets`)
- `RentalMapCapability` (`get_map_pins`)

### Dependency Inversion Principle (DIP)
High-level MCP tools depend entirely on the abstraction (`RentalProviderProtocol`), which is injected via constructors or factory methods.

---

## Design Patterns

1. **Adapter Pattern**: Translates Imobzi-specific JSON schema (`db_id`, `site_title`, `measure_type`, `useful_area`) into standardized MCP domain entities (`ListingPrice`, `RentalListing`, `RentalPropertyDetail`).
2. **Strategy Pattern**: The MCP server selects and executes search strategies across registered real estate providers.
3. **Value Object Pattern**: `ListingPrice`, `PropertyCode`, `GeoCoordinate`, and `RentalFilter` are immutable (`frozen=True`) value objects with built-in validation.
4. **First-Class Collection Pattern**: `RentalListingCollection` and `PhotoCollection` manage lists without exposing raw collections to external tampering.
5. **Builder Pattern**: `RentalQueryBuilder` cleanly constructs complex query parameter dictionaries step-by-step.
6. **Factory Pattern**: `CasaLinharesProviderFactory` encapsulates initialization of transport, resolver, query builder, and parsers.

---

## Consequences & Benefits

- **High Modularity**: Can be imported as an isolated Python package (`casalinhares_provider`) directly into any central MCP repository.
- **Robust Resilience**: Dynamic database namespace lookup ensures that even if Imobzi re-assigns tenant identifiers, the client self-heals by resolving the domain.
- **Zero Monolithic Bloat**: Strict adherence to size and calisthenics limits guarantees clean, readable, easily maintainable and testable code.
