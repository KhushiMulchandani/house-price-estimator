# 02 · SRS + Feature Specification

## 1. Scope
A web app that estimates a house price from four numeric inputs using a pre-trained regression model.

## 2. Users
Single role: **anonymous visitor**. No login.

## 3. Functional requirements

| ID | Requirement |
|---|---|
| FR-1 | The UI shall provide inputs for square footage, bedrooms, house age and location rating. |
| FR-2 | The UI shall send the values as JSON via `POST /api/v1/estimate/`. |
| FR-3 | The API shall validate every field (type and range) before prediction. |
| FR-4 | The API shall return `{ "estimated_price": <float> }` on success. |
| FR-5 | The API shall return HTTP 400 with per-field error messages on invalid input. |
| FR-6 | The UI shall display the price formatted as INR (e.g. `₹3,50,230.50`). |
| FR-7 | The UI shall show loading and error states. |
| FR-8 | The model shall be loaded once at server startup, not per request. |

## 4. Input rules

| Field | Key | Type | Allowed range |
|---|---|---|---|
| Square footage | `sqft` | number | 300 – 10,000 |
| Bedrooms | `bedrooms` | integer | 1 – 10 |
| House age (years) | `age` | number | 0 – 100 |
| Location rating | `location_rating` | integer | 1 – 5 |

Strings, nulls, missing fields and out-of-range values are rejected.

## 5. Non-functional requirements
- **Performance:** response under 1 s on a local machine.
- **Statelessness:** no database required for predictions.
- **Security:** CORS restricted to the frontend origin; model file loaded only from a trusted local path.
- **Usability:** works on desktop and mobile widths.
- **Maintainability:** ML training reproducible via a fixed random seed.

## 6. Out of scope
User accounts · saving estimates · maps/address lookup · real market data · production deployment

## 7. Assumptions
- Price is in INR.
- Model is trained on synthetic data, so the UI shows a disclaimer.

## 8. Acceptance criteria
- Entering `1500 / 3 / 10 / 4` returns a numeric price and displays it formatted.
- Entering `abc` for any field returns a 400 and an error message in the UI.
- All tests in [09-testing-security.md](09-testing-security.md) pass.
