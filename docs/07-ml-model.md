# 07 · ML Dataset + Model Design

## Problem
Regression: predict a continuous price (USD) from four features.

## Features

| Feature | Column | Type | Range |
|---|---|---|---|
| Square footage | `sqft` | float | 300 – 10,000 |
| Bedrooms | `bedrooms` | int | 1 – 10 |
| House age (years) | `age` | float | 0 – 100 |
| Location rating | `location_rating` | int | 1 – 5 |

**Feature order is a contract.** The model expects `[sqft, bedrooms, age, location_rating]` in exactly this order. The backend must build the array the same way.

**Target:** `price` (USD, float).

## Dataset (proposed: synthetic)
The sklearn built-in housing data does not contain these four features, so generate data in `train.py` with a fixed seed (`random_state=42`):

```
price = 50,000
      + 120   * sqft
      + 8,000 * bedrooms
      - 1,000 * age
      + 25,000 * location_rating
      + Normal(0, 15,000)      # noise
```

Row count: ~2,000. Clip prices to a positive minimum.

Alternative: use a public housing CSV and map columns to these features. If you do, document its source and licence here.

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

## Targets
| Metric | Target |
|---|---|
| R² | above 0.95 on synthetic data |
| MAE | within the noise level (about 12,000 USD) |

Record the actual results here after training.

## Risks and notes
- **Version drift:** pickles can fail across scikit-learn versions. Pin the version in `requirements.txt` for both `ml_model/` and `backend/`.
- **Synthetic data:** results do not reflect real housing markets; the UI says so.
- **Extrapolation:** linear models can produce odd values outside the training ranges, which is why inputs are range-validated.
- **Trust:** only load pickles you created yourself.
