# 06 · API Specification

**Base URL (dev):** `http://localhost:8000`
**Format:** JSON · **Auth:** none · **CORS:** `http://localhost:5173`

## POST `/api/v1/estimate/`

Returns an estimated house price.

### Request

Headers: `Content-Type: application/json`

```json
{
  "sqft": 1500,
  "bedrooms": 3,
  "age": 10,
  "location_rating": 4
}
```

| Field | Type | Required | Rule |
|---|---|---|---|
| `sqft` | number | yes | 300 to 10,000 |
| `bedrooms` | integer | yes | 1 to 10 |
| `age` | number | yes | 0 to 100 |
| `location_rating` | integer | yes | 1 to 5 |

### Success: `200 OK`

```json
{ "estimated_price": 350230.5 }
```

### Validation error: `400 Bad Request`

```json
{
  "sqft": ["Ensure this value is greater than or equal to 300."],
  "location_rating": ["A valid integer is required."]
}
```

### Other errors

| Status | When | Body |
|---|---|---|
| 400 | Missing, non-numeric or out-of-range field | Per-field messages (above) |
| 405 | Any method other than POST | `{ "detail": "Method \"GET\" not allowed." }` |
| 415 | Body is not JSON | `{ "detail": "Unsupported media type ..." }` |
| 500 | Model file missing or prediction failure | `{ "detail": "Prediction service unavailable." }` |

### cURL example

```bash
curl -X POST http://localhost:8000/api/v1/estimate/ \
  -H "Content-Type: application/json" \
  -d '{"sqft":1500,"bedrooms":3,"age":10,"location_rating":4}'
```

## Versioning
The `/api/v1/` prefix leaves room for breaking changes later (`/api/v2/`).

## Contract tests
Each row above must have a matching backend test (see [09-testing-security.md](09-testing-security.md)).
