from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from . import ml
from .serializers import EstimateRequestSerializer


class EstimateView(APIView):
    """POST /api/v1/estimate/  ->  { "estimated_price": <float, INR> }"""

    parser_classes = [JSONParser]  # non-JSON bodies get 415

    def post(self, request):
        serializer = EstimateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 400 with per-field errors

        try:
            price = ml.predict(serializer.validated_data)
        except ml.PredictionUnavailable:
            return Response(
                {"detail": "Prediction service unavailable."}, status=500
            )

        return Response({"estimated_price": round(price, 2)})
