"""Sanity tests for the trained model. Run from ml_model/:  pytest"""
import sys
from pathlib import Path

import joblib
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import train  # noqa: E402


@pytest.fixture(scope="module")
def trained(tmp_path_factory):
    """Train into a temp folder so tests never touch the real house_model.pkl."""
    out = tmp_path_factory.mktemp("model")
    summary = train.run(out_dir=out)
    model = joblib.load(out / "house_model.pkl")
    return model, summary


def row(sqft=1500, bedrooms=3, age=10, location_rating=4):
    # Column order is the contract: sqft, bedrooms, age, location_rating
    return pd.DataFrame(
        [[sqft, bedrooms, age, location_rating]], columns=train.FEATURES
    )


def test_feature_order_contract():
    assert train.FEATURES == ["sqft", "bedrooms", "age", "location_rating"]


def test_model_file_loads_and_predicts_one_float(trained):
    model, _ = trained
    pred = model.predict(row())
    assert pred.shape == (1,)
    assert isinstance(float(pred[0]), float)


def test_larger_sqft_gives_higher_price(trained):
    model, _ = trained
    assert model.predict(row(sqft=2500))[0] > model.predict(row(sqft=800))[0]


def test_older_house_is_not_pricier(trained):
    model, _ = trained
    assert model.predict(row(age=80))[0] <= model.predict(row(age=5))[0]


def test_better_location_gives_higher_price(trained):
    model, _ = trained
    assert model.predict(row(location_rating=5))[0] > model.predict(row(location_rating=1))[0]


def test_price_is_positive_across_valid_range(trained):
    model, _ = trained
    corners = [
        row(300, 1, 100, 1),
        row(10_000, 10, 0, 5),
        row(300, 10, 100, 1),
        row(10_000, 1, 0, 5),
    ]
    for r in corners:
        assert model.predict(r)[0] > 0


def test_metrics_meet_target(trained):
    _, summary = trained
    best = summary["metrics"][summary["best_model"]]
    assert best["r2"] > 0.95


def test_training_is_reproducible(tmp_path):
    a = train.run(out_dir=tmp_path / "a")["metrics"]
    b = train.run(out_dir=tmp_path / "b")["metrics"]
    for name in a:
        for metric in a[name]:
            assert a[name][metric] == pytest.approx(b[name][metric], rel=1e-9)
