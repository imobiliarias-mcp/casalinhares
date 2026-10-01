# Casa Linhares — Rental API Reverse Engineering Documentation

Welcome to the reverse-engineering and architecture documentation for **Casa Linhares e Corretores Associados** (`https://www.casalinhares.com.br/`).

This repository contains the reverse-engineered API specifications, architectural decision records, and clean, modular Python components designed for integration into a **Central Rental Research MCP (Model Context Protocol)** server.

---

## Documentation Structure

- **[Single Source of Truth API Specification](file:///home/samuelcaldas/repos/imobiliarias/casalinhares/docs/sot/imobzi_casalinhares_api_spec.md)** (`docs/sot/imobzi_casalinhares_api_spec.md`):
  Comprehensive contract specification for all endpoints, headers, payload schemas, query matrices, and authentication rules.

- **[Architecture Decision Record 0001](file:///home/samuelcaldas/repos/imobiliarias/casalinhares/docs/adr/0001-rental-search-mcp-module-design.md)** (`docs/adr/0001-rental-search-mcp-module-design.md`):
  Detailed rationale on Ports-and-Adapters (Hexagonal) architecture, SOLID principles, Design Patterns, and strict Object Calisthenics enforcement.

- **[API Reference & Quick Recipes](file:///home/samuelcaldas/repos/imobiliarias/casalinhares/docs/api_reference.md)** (`docs/api_reference.md`):
  Developer reference featuring ready-to-run `curl` commands, parameter dictionaries, and implementation tips.

- **[Scripts & MCP Module Guide](file:///home/samuelcaldas/repos/imobiliarias/casalinhares/scripts/README.md)** (`scripts/README.md`):
  Developer guide for running the Python modules, CLI utilities, and MCP tool handlers.

---

## Key Technical Discoveries Summary

| Dimension | Discovery |
|:---|:---|
| **Underlying Platform** | Imobzi (SaaS Real Estate Portal Engine) |
| **API Host** | `https://api2.imobzi.app/v1` |
| **Account Discovery** | `GET https://api2.imobzi.app/v1/site/database/www.casalinhares.com.br` |
| **Tenant Database ID** | `ac-ohlj221031aqut` |
| **Authentication Requirement** | Origin/Referer check (`Origin: https://www.casalinhares.com.br`) |
| **Search Endpoint** | `GET /v1/{database}/site2/search/properties?availability=rent` |
| **Facets Endpoint** | `GET /v1/{database}/site2/properties/search/fields` |
| **Map Endpoint** | `GET /v1/{database}/site2/search/map` |
| **Property Detail Endpoint** | `GET /v1/{database}/site2/properties/{code}` |
| **Pagination Model** | Dual: Keyset JWT cursor (`cursor=...`) and 1-based page index (`page=N`) |
