# Imobzi Real Estate Platform API Specification — Casa Linhares

## 1. Overview & Architecture

This document serves as the **Single Source of Truth (SOT)** for the reverse-engineered rental search and property management APIs powering **Casa Linhares e Corretores Associados** (`https://www.casalinhares.com.br/`).

### 1.1 Platform Identification

- **SaaS Vendor**: [Imobzi](https://www.imobzi.com/) (real estate CRM & portal SaaS platform)
- **Frontend Framework**: Angular Universal (SSR with client-side hydration, Angular TransferState via `<script id="ng-state" type="application/json">`)
- **API Base URL**: `https://api2.imobzi.app/v1`
- **Asset / Media CDN**:
  - `https://media.imobzi.com`
  - `https://imobzi.storage.googleapis.com`
- **Tenant Database Namespace**: `ac-ohlj221031aqut` (discovered dynamically via domain lookup)

### 1.2 Authentication & Access Control

The Imobzi public site API does not require Bearer tokens or static API keys for public listing endpoints. Instead, access control is enforced at the Cloudflare / Express gateway level using origin validation:

- **Mandatory Headers**:
  - `Origin: https://www.casalinhares.com.br`
  - `Referer: https://www.casalinhares.com.br/`
  - `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...`

> **Note on Security Behavior**: Requests omitting the `Origin` header receive `HTTP 401 Unauthorized`:
> ```json
> {"message": "Not permitted"}
> ```
> Including `Origin: https://www.casalinhares.com.br` grants full `HTTP 200 OK` access to search and property data.

---

## 2. Dynamic Tenant Discovery

Any Imobzi tenant website domain can be dynamically resolved to its internal account database namespace.

### Endpoint: Database Lookup
- **URL**: `GET https://api2.imobzi.app/v1/site/database/{hostname}`
- **Headers**:
  - `Origin: https://{hostname}`
  - `Referer: https://{hostname}/`
- **Parameters**:
  - `hostname` (path parameter): Domain name (e.g., `www.casalinhares.com.br`)

#### Response Schema (`HTTP 200`):
```json
{
  "database": "ac-ohlj221031aqut",
  "logo_url": "https://imobzi.storage.googleapis.com/accounts/ac-ohlj221031aqut/public/logo.png",
  "in_construction": false,
  "color_primary": "#252973"
}
```

The returned `database` string is used as the tenant identifier path component for all subsequent API requests:
`https://api2.imobzi.app/v1/{database}/site2/...`

---

## 3. Endpoints Catalog

### 3.1 Rental Properties Search (List)

Searches properties with filtering, sorting, and pagination.

- **URL**: `GET https://api2.imobzi.app/v1/{database}/site2/search/properties`
- **Headers**: `Origin`, `Referer`, `User-Agent`
- **Query Parameters**:

| Parameter | Type | Required | Default | Description |
|:---|:---|:---:|:---:|:---|
| `availability` | `string` | Yes | `rent` | Transaction type: `rent` (locação), `sale` (venda), or `rent,sale` |
| `order` | `string` | No | `created_at` | Sorting attribute: `created_at`, `rental_value`, `area`, `sale_value` |
| `direction` | `string` | No | `desc` | Direction: `asc` or `desc` |
| `page` | `integer` | No | `1` | Page index (1-based) |
| `cursor` | `string` | No | - | Opaque JWT pagination token from previous page response |
| `with_photos` | `string` | No | `true` | Include `photos` collection with full URLs |
| `with_listing_broker_count` | `string` | No | `true` | Include broker details and total active listings count |
| `city` | `string` | No | - | City name (e.g. `Timóteo`, `Ipatinga`). Repeatable for multi-city search. |
| `neighborhood` | `string` | No | - | Neighborhood name. Repeatable for multi-neighborhood. |
| `property_type` | `string` | No | - | Property type (e.g. `Apartamento`, `Casa`, `Loja / Salão`). Repeatable. |
| `finality` | `string` | No | - | Purpose: `residential`, `commercial`, `industrial`, `rural`. Repeatable. |
| `bedroom_gte` | `integer` | No | - | Minimum bedroom count (greater than or equal). |
| `bedroom` | `integer` | No | - | Exact bedroom count. Repeatable. |
| `bathroom_gte` | `integer` | No | - | Minimum bathroom count. |
| `suite_gte` | `integer` | No | - | Minimum suite count. |
| `garage_gte` | `string` | No | - | Minimum garage spaces (`1`, `2`) or `"no_garage"`. |
| `value_min` | `number` | No | - | Minimum price in BRL. |
| `value_max` | `number` | No | - | Maximum price in BRL. |
| `area_min` | `number` | No | - | Minimum area in square meters. |
| `area_max` | `number` | No | - | Maximum area in square meters. |
| `feature` | `string` | No | - | Feature ID/code (amenities). Repeatable. |
| `building_name` | `string` | No | - | Building or condominium name filter. |

#### Response Schema:
```json
{
  "properties": {
    "cursor": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "count": 28,
    "properties": [
      {
        "db_id": "5018138942373888",
        "code": "1443",
        "site_title": "Loja / Salão em Quitandinha  -  Timóteo",
        "site_url": "/imovel/loja-salao-quitandinha-timoteo-code-1443",
        "property_type": "Loja / Salão",
        "finality": "commercial",
        "neighborhood": "Quitandinha",
        "city": "Timóteo",
        "state": "MG",
        "country": "Brasil",
        "latitude": -19.58,
        "longitude": -42.63,
        "rental_value": 1500.0,
        "sale_value": 0.0,
        "total_rental_value": 0,
        "area": 50.0,
        "useful_area": 50.0,
        "lot_area": 0.0,
        "measure_type": "M²",
        "bedroom": 0,
        "bathroom": 1,
        "suite": 0,
        "garage": 0,
        "building": false,
        "building_name": "",
        "status": "available",
        "vacation_rental": false,
        "site_publish_price": true,
        "site_publish_rental_price": true,
        "cover_photo": {
          "db_id": "6466774771433472",
          "url": "https://media.imobzi.com/..."
        },
        "photos": [
          {
            "url": "https://media.imobzi.com/...",
            "description": ""
          }
        ],
        "listing_broker": {
          "db_id": "XXHaG7XfscgbFjHd0vH5N7RCZ3x1",
          "name": "Henrique Americano",
          "nickname": "henriqueamericano",
          "email": "regisousa@yahoo.com.br",
          "phones": [
            {
              "type": "mobile",
              "number": "(31) 98481-1069",
              "country_code": "+55",
              "alpha2Code": "br"
            }
          ],
          "count": 78
        }
      }
    ],
    "fields": null
  }
}
```

---

### 3.2 Search Filter Facets & Counts (Aggregations)

Retrieves all available search facets, available cities, neighborhoods, property types, price ranges, and counts for a given filter.

- **URL**: `GET https://api2.imobzi.app/v1/{database}/site2/properties/search/fields`
- **Query Parameters**:
  - `availability=rent`
  - `direction=desc`
  - `order=created_at`
  - `all_fields=true`
  - `filters_show_total=true`
  - `search_type=filter_without_count`

#### Response Schema:
```json
{
  "cities": ["Ipatinga - MG", "Timóteo - MG"],
  "neighborhoods": [
    "Alvorada, Timóteo - MG",
    "Cachoeira do Vale, Timóteo - MG",
    "Canaã, Ipatinga - MG",
    "Centro, Timóteo - MG",
    "Funcionários, Timóteo - MG",
    "Horto, Ipatinga - MG",
    "Iguaçu, Ipatinga - MG",
    "Quitandinha, Timóteo - MG",
    "São Geraldo, Timóteo - MG",
    "Timirim, Timóteo - MG",
    "Veneza, Ipatinga - MG",
    "Vila dos Técnicos, Timóteo - MG"
  ],
  "property_types": [
    {
      "property_finality": "residential",
      "types": ["Apartamento", "Casa", "Cobertura"]
    },
    {
      "property_finality": "commercial",
      "types": [
        "Conjunto / Sala",
        "Galpão / Depósito / Armazém",
        "Loja / Salão",
        "Loja Shopping / Centro Comercial"
      ]
    }
  ],
  "areas": { "min": 0, "max": 1800 },
  "values": { "min": 0, "max": 27000 },
  "buildings": ["CONJUNTO DE SALAS COMERCIAL"],
  "bedrooms": [true, true, true, true, true],
  "bathrooms": [true, true, true, true, true],
  "suites": [true, true, true, true, true],
  "garages": [true, true, true, true, true],
  "availability": ["buy", "rent", "vacation_rental"],
  "total": 28
}
```

---

### 3.3 Map Search Pins

Retrieves map coordinates and compact card payloads for all matching properties.

- **URL**: `GET https://api2.imobzi.app/v1/{database}/site2/search/map`
- **Query Parameters**:
  - `availability=rent`
  - `direction=desc`
  - `order=created_at`
  - `get_center_map=true`

#### Response Schema:
```json
{
  "map_center": {
    "lat": -19.519023881293833,
    "lon": -42.611135483408965
  },
  "properties_map": [
    {
      "db_id": "5018138942373888",
      "code": "1443",
      "latitude": -19.58,
      "longitude": -42.63,
      "site_title": "Loja / Salão em Quitandinha  -  Timóteo",
      "site_url": "/imovel/loja-salao-quitandinha-timoteo-code-1443",
      "property_type": "Loja / Salão",
      "neighborhood": "Quitandinha",
      "city": "Timóteo",
      "state": "MG",
      "rental_value": 1500.0,
      "sale_value": 0.0,
      "useful_area": 50.0,
      "area": 50.0,
      "cover_photo": {
        "url": "https://media.imobzi.com/..."
      }
    }
  ]
}
```

---

### 3.4 Property Detail by Code

Fetches exhaustive details for an individual property using its business code (e.g., `1443`).

- **URL**: `GET https://api2.imobzi.app/v1/{database}/site2/properties/{code}`
- **Query Parameters**:
  - `listing_broker_properties_count=true`

#### Key Response Attributes:
- `code`: Business listing code (e.g. `"1443"`).
- `db_id`: Database primary key identifier.
- `site_title`: Public display title.
- `site_description`: HTML rich description.
- `description`: Plain text description.
- `site_url`: Canonical slug path.
- `property_type`: Property classification.
- `finality`: `residential` or `commercial`.
- `rental_value`: Monthly rent in BRL.
- `sale_value`: Sale price in BRL (if also for sale).
- `value_to_fire_insurance`: Fire insurance estimated cost.
- `iptu_installments`: IPTU municipal tax installments.
- `area`, `useful_area`, `lot_area`, `measure_type`: Dimensions.
- `bedroom`, `bathroom`, `suite`, `garage`: Numeric amenities.
- `city`, `neighborhood`, `state`, `country`, `latitude`, `longitude`: Location.
- `photos`: Complete gallery array with high-resolution image URLs.
- `listing_broker`: Direct agent contact object (name, email, phone numbers, total portfolio count).
- `status`: Availability flag (`available`, `rented`, etc.).
- `created_at`, `updated_at`: Timestamps.

---

### 3.5 Related Properties

Fetches recommended similar properties for a given property listing.

- **URL**: `GET https://api2.imobzi.app/v1/{database}/site2/properties/{code}/related`
- **Response**: Array of property summaries similar to the target listing.

---

### 3.6 Property Amenities & Features Catalog

Returns the global taxonomy of property features/amenities supported by the tenant.

- **URL**: `GET https://api2.imobzi.app/v1/{database}/site2/property-features`
- **Response**: Array of strings (e.g. `["Ar condicionado", "Armário cozinha", "Elevador", "Interfone", "Piscina", ...]`).

---

### 3.7 Property Neighborhoods with Listing Counts

Returns neighborhoods partitioned with their respective active property counts.

- **URL**: `GET https://api2.imobzi.app/v1/{database}/site2/property-neighborhoods?with_properties_count=true`
- **Response**:
```json
{
  "properties_count": 142,
  "properties_neighborhood": [
    { "neighborhood": "Centro", "city": "Timóteo", "count": 28 },
    { "neighborhood": "Horto", "city": "Ipatinga", "count": 19 }
  ]
}
```

---

### 3.8 Lead Contact & Visit Scheduling Submission

Submits contact inquiries or visit bookings directly to Imobzi CRM.

- **URL**: `POST https://api2.imobzi.app/v1/{database}/site/form-contact`
- **Content-Type**: `multipart/form-data`
- **Fields**:
  - `name`: Full name of inquirer.
  - `phone`: Contact phone number formatted as `(XX) XXXXX-XXXX`.
  - `email`: Valid email address.
  - `message`: Inquirer's message or auto-generated visit text.
  - `property_code`: Property code being queried.
  - `iam_human`: `""` (**Honeypot field — MUST remain empty**).

---

## 4. Pagination Strategy

The Imobzi search endpoint supports two independent pagination strategies:

1. **Page-Number Pagination**:
   - `page=1`, `page=2`, etc.
   - Page size is fixed by backend (18 items per page for search).
   - Once the last page is reached, `cursor` in the response becomes `null` or omitted.

2. **Keyset / Cursor Pagination**:
   - In each response, `properties.cursor` contains a JWT string.
   - Passing `cursor={token}` on the subsequent request retrieves the next page.
   - Cursor payload structure (decoded):
     ```json
     {"created_at": 1736189729, "db_key": "5542651395309568", "order": "created_at"}
     ```
   - When `cursor` is `null`, pagination is complete.

---

## 5. Status Codes & Error Handling

| Status Code | Meaning | Cause | Remediation |
|:---:|:---|:---|:---|
| `200` | OK | Successful query | Parse JSON payload |
| `401` | Not Permitted | Missing or invalid `Origin` header | Ensure `Origin: https://www.casalinhares.com.br` is supplied |
| `404` | Not Found | Unknown property code or invalid endpoint | Verify property code exists |
| `422` / `400` | Bad Request | Malformed parameter or type mismatch | Validate parameter types before sending |
| `5xx` | Gateway / Upstream Error | Imobzi service disruption | Implement exponential backoff retry |
