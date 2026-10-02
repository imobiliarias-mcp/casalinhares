# Imobzi / Casa Linhares API Quick Reference

This document provides quick reference documentation, parameter matrices, and ready-to-execute `curl` recipes for developers integrating Casa Linhares rental data.

---

## 1. Quick Recipes (cURL)

### 1.1 Tenant Database Discovery
```bash
curl -s "https://api2.imobzi.app/v1/site/database/www.casalinhares.com.br" \
  -H "Origin: https://www.casalinhares.com.br" \
  -H "Referer: https://www.casalinhares.com.br/"
```

### 1.2 Search All Active Rentals (Sorted by Most Recent)
```bash
curl -s "https://api2.imobzi.app/v1/ac-ohlj221031aqut/site2/search/properties?availability=rent&order=created_at&direction=desc&with_photos=true&with_listing_broker_count=true" \
  -H "Origin: https://www.casalinhares.com.br" \
  -H "Referer: https://www.casalinhares.com.br/"
```

### 1.3 Search Rentals with Price & Bedroom Filters
```bash
curl -s "https://api2.imobzi.app/v1/ac-ohlj221031aqut/site2/search/properties?availability=rent&city=Tim%C3%B3teo&bedroom_gte=2&value_min=1000&value_max=3000&with_photos=true" \
  -H "Origin: https://www.casalinhares.com.br" \
  -H "Referer: https://www.casalinhares.com.br/"
```

### 1.4 Get Available Search Facets (Aggregated Filters)
```bash
curl -s "https://api2.imobzi.app/v1/ac-ohlj221031aqut/site2/properties/search/fields?availability=rent&all_fields=true&filters_show_total=true&search_type=filter_without_count" \
  -H "Origin: https://www.casalinhares.com.br" \
  -H "Referer: https://www.casalinhares.com.br/"
```

### 1.5 Get Rental Property Map Pins
```bash
curl -s "https://api2.imobzi.app/v1/ac-ohlj221031aqut/site2/search/map?availability=rent&direction=desc&order=created_at&get_center_map=true" \
  -H "Origin: https://www.casalinhares.com.br" \
  -H "Referer: https://www.casalinhares.com.br/"
```

### 1.6 Get Full Property Details by Code
```bash
curl -s "https://api2.imobzi.app/v1/ac-ohlj221031aqut/site2/properties/1443?listing_broker_properties_count=true" \
  -H "Origin: https://www.casalinhares.com.br" \
  -H "Referer: https://www.casalinhares.com.br/"
```

### 1.7 Get Similar / Related Properties
```bash
curl -s "https://api2.imobzi.app/v1/ac-ohlj221031aqut/site2/properties/1443/related" \
  -H "Origin: https://www.casalinhares.com.br" \
  -H "Referer: https://www.casalinhares.com.br/"
```

---

## 2. Parameter Matrix for Rental Searches

| Query Parameter | Format / Values | Example |
|:---|:---|:---|
| `availability` | `rent` \| `sale` \| `rent,sale` | `availability=rent` |
| `order` | `created_at` \| `rental_value` \| `area` | `order=created_at` |
| `direction` | `desc` \| `asc` | `direction=desc` |
| `page` | Integer ≥ 1 | `page=2` |
| `cursor` | JWT Base64URL string | `cursor=eyJhbGci...` |
| `city` | Text (repeatable) | `city=Timóteo&city=Ipatinga` |
| `neighborhood` | Text (repeatable) | `neighborhood=Centro` |
| `property_type` | Text (repeatable) | `property_type=Apartamento` |
| `finality` | `residential` \| `commercial` | `finality=residential` |
| `bedroom_gte` | Integer ≥ 0 | `bedroom_gte=2` |
| `bathroom_gte` | Integer ≥ 0 | `bathroom_gte=1` |
| `garage_gte` | Integer ≥ 0 or `no_garage` | `garage_gte=1` |
| `value_min` | Numeric (BRL) | `value_min=1200` |
| `value_max` | Numeric (BRL) | `value_max=3500` |
| `area_min` | Numeric ($m^2$) | `area_min=60` |
| `area_max` | Numeric ($m^2$) | `area_max=200` |
| `with_photos` | Boolean string (`true`/`false`) | `with_photos=true` |
| `with_listing_broker_count` | Boolean string (`true`/`false`) | `with_listing_broker_count=true` |

---

## 3. Important Implementation Notes

1. **Origin Header Enforcement**: Every request to `api2.imobzi.app` MUST pass `Origin: https://www.casalinhares.com.br`. Without this header, Cloudflare returns `401 {"message": "Not permitted"}`.
2. **Page vs. Cursor Pagination**: Both `page=N` and `cursor=TOKEN` work. `page=N` is easiest for random page jumps, while `cursor` guarantees consistency across concurrent listing inserts.
3. **Price Field**: For rental searches, inspect `rental_value`. The `total_rental_value` field is often `0` if condominium and IPTU taxes are paid separately by the tenant.
4. **Photo Resolution**: Image URLs from `media.imobzi.com` can have `=s0` appended for original resolution or `=s400` for 400px thumbnails.

## 4. Public Property URLs

Search results expose the public listing destination in the API-provided `site_url` field.
The adapter resolves relative or protocol-relative values against its configured Casa Linhares
site origin and serializes the absolute HTTP(S) destination as `url`, while retaining the
existing `media_url` field. It does not construct a property route from the listing code or
make an extra detail request. Missing links, Imobzi API endpoints, media files, and non-property
site routes raise a contextual `ValueError` instead of being returned as property URLs.

```python
for listing in search_result.listings():
    print(listing.to_dictionary()["url"])
```
