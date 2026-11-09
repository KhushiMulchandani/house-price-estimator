# 04 · Database Design + ER Diagram

## Status: not applicable for v1.0

The API is **stateless**. Predictions are computed from the request body and the pickled model, so no tables are needed. Django's default SQLite file exists only for framework internals and is git-ignored.

## Optional future extension

If you later want to log estimates (for history or analytics), add one table:

```
┌────────────────────────────┐
│ Prediction                 │
├────────────────────────────┤
│ id            PK           │
│ sqft          FLOAT        │
│ bedrooms      INT          │
│ age           FLOAT        │
│ location_rating INT        │
│ estimated_price FLOAT      │
│ model_version VARCHAR      │
│ created_at    DATETIME     │
└────────────────────────────┘
```

This adds a migration, a model, and a decision about privacy. It is intentionally **out of scope** for v1.0.
