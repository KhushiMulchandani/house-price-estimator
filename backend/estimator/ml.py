"""Loads the trained model ONCE (when Django starts) and exposes predict().

SECURITY: house_model.pkl is a pickle. Only load a file you trained yourself,
from the fixed path in settings.MODEL_PATH. Never load uploaded pickles.
"""
import logging

import joblib
import pandas as pd
from django.conf import settings

logger = logging.getLogger(__name__)

# Contract with ml_model/train.py: the model expects columns in THIS order.
FEATURES = ["sqft", "bedrooms", "age", "location_rating"]


class PredictionUnavailable(Exception):
    """Raised when the model is missing or the prediction fails."""


def _load_model():
    try:
        return joblib.load(settings.MODEL_PATH)
    except Exception:
        logger.exception("Could not load model from %s", settings.MODEL_PATH)
        return None


_model = _load_model()  # runs once, at import time


def predict(data: dict) -> float:
    """data: validated dict with the four feature keys. Returns price in INR."""
    if _model is None:
        raise PredictionUnavailable("Model not loaded")
    try:
        # DataFrame (not a bare array) so column names match training.
        row = pd.DataFrame([[data[name] for name in FEATURES]], columns=FEATURES)
        return float(_model.predict(row)[0])
    except Exception as exc:
        logger.exception("Prediction failed")
        raise PredictionUnavailable("Prediction failed") from exc
