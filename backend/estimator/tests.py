"""API tests. Cases mirror docs/06-api-spec.md and docs/09-testing-security.md.

Needs ml_model/house_model.pkl to exist (run ml_model/train.py first).
"""
from unittest import mock

from django.test import SimpleTestCase
from rest_framework.test import APIClient

from . import ml

URL = "/api/v1/estimate/"
VALID = {"sqft": 1500, "bedrooms": 3, "age": 10, "location_rating": 4}

# (field, too_low, too_high)
RANGES = [
    ("sqft", 299, 10_001),
    ("bedrooms", 0, 11),
    ("age", -1, 101),
    ("location_rating", 0, 6),
]


class EstimateApiTests(SimpleTestCase):
    def setUp(self):
        self.client = APIClient()

    def post(self, payload):
        return self.client.post(URL, payload, format="json")

    def test_valid_payload_returns_price(self):
        res = self.post(VALID)
        self.assertEqual(res.status_code, 200)
        price = res.json()["estimated_price"]
        self.assertIsInstance(price, float)
        # Sanity band around the training formula (~87 lakh for this input)
        self.assertTrue(7_000_000 < price < 10_500_000, price)

    def test_missing_field_returns_400_naming_field(self):
        for field in VALID:
            with self.subTest(field=field):
                payload = {k: v for k, v in VALID.items() if k != field}
                res = self.post(payload)
                self.assertEqual(res.status_code, 400)
                self.assertIn(field, res.json())

    def test_string_instead_of_number_returns_400(self):
        for field in VALID:
            with self.subTest(field=field):
                res = self.post({**VALID, field: "abc"})
                self.assertEqual(res.status_code, 400)
                self.assertIn(field, res.json())

    def test_null_returns_400(self):
        res = self.post({**VALID, "sqft": None})
        self.assertEqual(res.status_code, 400)

    def test_out_of_range_returns_400(self):
        for field, low, high in RANGES:
            for bad in (low, high):
                with self.subTest(field=field, value=bad):
                    res = self.post({**VALID, field: bad})
                    self.assertEqual(res.status_code, 400)
                    self.assertIn(field, res.json())

    def test_boundary_values_are_accepted(self):
        for payload in (
            {"sqft": 300, "bedrooms": 1, "age": 0, "location_rating": 1},
            {"sqft": 10_000, "bedrooms": 10, "age": 100, "location_rating": 5},
        ):
            with self.subTest(payload=payload):
                self.assertEqual(self.post(payload).status_code, 200)

    def test_non_integer_bedrooms_and_rating_return_400(self):
        for field in ("bedrooms", "location_rating"):
            with self.subTest(field=field):
                res = self.post({**VALID, field: 2.5})
                self.assertEqual(res.status_code, 400)
                self.assertIn(field, res.json())

    def test_get_returns_405(self):
        self.assertEqual(self.client.get(URL).status_code, 405)

    def test_non_json_body_returns_415(self):
        res = self.client.post(URL, "sqft=1500", content_type="text/plain")
        self.assertEqual(res.status_code, 415)

    def test_model_unavailable_returns_500_with_generic_message(self):
        with mock.patch(
            "estimator.views.ml.predict", side_effect=ml.PredictionUnavailable
        ):
            res = self.post(VALID)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.json(), {"detail": "Prediction service unavailable."})
