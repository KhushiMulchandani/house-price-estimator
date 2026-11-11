# 03 · System Architecture

## Overview

```
┌──────────────┐  JSON POST   ┌─────────────────┐  load once   ┌──────────────────┐
│ React (Vite) │ ───────────► │ Django + DRF    │ ───────────► │ house_model.pkl  │
│ :5173        │ ◄─────────── │ :8000           │ ◄─────────── │ (scikit-learn)   │
└──────────────┘  JSON price  └─────────────────┘  prediction  └──────────────────┘
```

## Request lifecycle
1. User fills the form and clicks **Estimate Price**.
2. React builds a JSON object and sends it with Axios.
3. Django validates it with a DRF serializer.
4. The view builds a 2D NumPy array `[[sqft, bedrooms, age, rating]]`.
5. The pre-loaded model returns a float.
6. Django responds `{ "estimated_price": 350230.50 }`.
7. React updates state and renders the formatted amount.

## Components

| Layer | Folder | Responsibility |
|---|---|---|
| ML | `ml_model/` | Generate data, train, evaluate, save `house_model.pkl` |
| Backend | `backend/` | Validate input, load model once, serve the endpoint, CORS |
| Frontend | `frontend/` | Form, Axios call, loading/error/result UI |

## Backend design
- Django project `config`, app `estimator`.
- `serializers.py`: `EstimateRequestSerializer` with range validators.
- `views.py`: `EstimateView(APIView)` handling `POST`.
- `ml.py`: loads the model with `joblib.load` at import time and exposes `predict(features)`.
- `settings.py`: `CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]`.

## Frontend design
- `PriceEstimatorForm`: one state object `{ sqft, bedrooms, age, location_rating }`.
- `ResultBox`: renders when a price exists, using `toLocaleString('en-IN', { style: 'currency', currency: 'INR' })`.
- `api.js`: Axios instance with base URL from `VITE_API_URL`.

## Configuration
| Variable | Where | Example |
|---|---|---|
| `DJANGO_SECRET_KEY` | backend `.env` | random string |
| `DJANGO_DEBUG` | backend `.env` | `True` |
| `MODEL_PATH` | backend `.env` | `../ml_model/house_model.pkl` |
| `VITE_API_URL` | frontend `.env` | `http://localhost:8000` |

Commit `.env.example` files only, never `.env`.

## Key decisions
| Decision | Choice | Reason |
|---|---|---|
| Database | None | Stateless predictions |
| Model loading | Once at startup | Avoid per-request disk reads |
| Repo layout | Monorepo | One place for docs, issues and PRs |
| Model format | joblib `.pkl` | Simple; pin scikit-learn version |
