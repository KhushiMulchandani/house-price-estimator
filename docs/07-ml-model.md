# 07 · ML Dataset + Model Design

## Problem
Regression: predict a continuous price (INR) from four features.

## Features

| Feature | Column | Type | Range |
|---|---|---|---|
| Square footage | `sqft` | float | 300 – 10,000 |
| Bedrooms | `bedrooms` | int | 1 – 10 |
| House age (years) | `age` | float | 0 – 100 |
| Location rating | `location_rating` | int | 1 – 5 |

**Feature order is a contract.** The model expects `[sqft, bedrooms, age, location_rating]` in exactly this order. The backend must build the array the same way.

**Target:** `price` (INR, float).

## Dataset (proposed: synthetic)
The sklearn built-in housing data does not contain these four features, so generate data in `train.py` with a fixed seed (`random_state=42`):

```
price = 5,00,000
      + 3500   * sqft
      + 2,50,000 * bedrooms
      - 20,000 * age
      + 6,00,000 * location_rating
      + Normal(0, 4,00,000)       # noise
```

Row count: ~2,000 rows, prices clipped to a minimum of ₹5,00,000, random_state=42.


## Model candidates

| Model | Pros | Cons |
|---|---|---|
| `LinearRegression` | Simple, fast, interpretable; matches the synthetic formula | Can't capture non-linear effects |
| `RandomForestRegressor` | Handles non-linearity | Larger file, slower, less interpretable |

**Plan:** train both, compare on the test set, ship the better one. Linear regression is expected to win on this synthetic data because the target is linear.

## Training pipeline (`ml_model/train.py`)
1. Generate or load data.
2. Split 80/20 train/test (`random_state=42`).
3. Fit each candidate.
4. Evaluate on the test set: **R²**, **MAE**, **RMSE**.
5. Save the chosen model with `joblib.dump` to `house_model.pkl`.
6. Print metrics and the scikit-learn version used.

## Targets and results

| Metric | Target | Result (LinearRegression) | Met? |
|---|---|---|---|
| R² | above 0.95 | 0.9982 | Yes |
| MAE | about ₹4,00,000 | ₹3,27,651 | Yes |

### Model comparison (20% test set, 400 rows)

| Model | R² | MAE (₹) | RMSE (₹) |
|---|---|---|---|
| **LinearRegression** (selected) | 0.9982 | 3,27,651 | 4,13,394 |
| RandomForestRegressor | 0.9958 | 5,13,560 | 6,39,392 |

**Decision:** LinearRegression is selected. It scores higher on every metric, and it is simpler and gives a smaller, faster model file. This is expected, because the synthetic prices follow a linear formula.

**Reproducibility:** seed 42, scikit-learn 1.9.1. Full numbers are in `ml_model/model_metrics.json`.

## Risks and notes
- **Version drift:** pickles can fail across scikit-learn versions. Pin the version in `requirements.txt` for both `ml_model/` and `backend/`.
- **Synthetic data:** results do not reflect real housing markets; the UI says so.
- **Extrapolation:** linear models can produce odd values outside the training ranges, which is why inputs are range-validated.
- **Trust:** only load pickles you created yourself.
