"""Train the House Price Estimator model on synthetic data (prices in INR).

Run from the ml_model/ folder:
    python train.py

Outputs (next to this file):
    house_model.pkl      the best model, saved with joblib
    model_metrics.json   metrics for both candidates + metadata
"""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

SEED = 42
N_ROWS = 2000
TEST_SIZE = 0.2

# The model expects columns in EXACTLY this order. The backend must match it.
FEATURES = ["sqft", "bedrooms", "age", "location_rating"]
TARGET = "price"

MIN_PRICE = 500_000  # INR floor so noise never produces a negative price
OUT_DIR = Path(__file__).resolve().parent


def generate_data(n_rows: int = N_ROWS, seed: int = SEED) -> pd.DataFrame:
    """Create a synthetic dataset. Ranges match docs/02-srs.md."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "sqft": rng.uniform(300, 10_000, n_rows).round(0),
            "bedrooms": rng.integers(1, 11, n_rows),         # 1..10
            "age": rng.uniform(0, 100, n_rows).round(1),
            "location_rating": rng.integers(1, 6, n_rows),   # 1..5
        }
    )
    noise = rng.normal(0, 400_000, n_rows)
    df[TARGET] = (
        500_000
        + 3_500 * df["sqft"]
        + 250_000 * df["bedrooms"]
        - 20_000 * df["age"]
        + 600_000 * df["location_rating"]
        + noise
    ).clip(lower=MIN_PRICE)
    return df


def evaluate(model, X_test, y_test) -> dict:
    pred = model.predict(X_test)
    return {
        "r2": float(r2_score(y_test, pred)),
        "mae": float(mean_absolute_error(y_test, pred)),
        "rmse": float(mean_squared_error(y_test, pred) ** 0.5),
    }


def run(out_dir: Path = OUT_DIR) -> dict:
    """Train both candidates, save the better one, return the summary."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = generate_data()
    X_train, X_test, y_train, y_test = train_test_split(
        df[FEATURES], df[TARGET], test_size=TEST_SIZE, random_state=SEED
    )

    candidates = {
        "LinearRegression": LinearRegression(),
        "RandomForestRegressor": RandomForestRegressor(
            n_estimators=200, random_state=SEED, n_jobs=-1
        ),
    }

    results, fitted = {}, {}
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        results[name] = evaluate(model, X_test, y_test)
        fitted[name] = model

    best_name = max(results, key=lambda n: results[n]["r2"])
    joblib.dump(fitted[best_name], out_dir / "house_model.pkl")

    summary = {
        "best_model": best_name,
        "currency": "INR",
        "features": FEATURES,
        "seed": SEED,
        "n_rows": N_ROWS,
        "test_size": TEST_SIZE,
        "scikit_learn_version": sklearn.__version__,
        "metrics": results,
    }
    (out_dir / "model_metrics.json").write_text(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    summary = run()
    print(f"scikit-learn version: {summary['scikit_learn_version']}")
    print(f"{'Model':<24}{'R2':>8}{'MAE (INR)':>16}{'RMSE (INR)':>16}")
    for name, m in summary["metrics"].items():
        print(f"{name:<24}{m['r2']:>8.4f}{m['mae']:>16,.0f}{m['rmse']:>16,.0f}")
    print(f"\nSaved best model: {summary['best_model']} -> house_model.pkl")
