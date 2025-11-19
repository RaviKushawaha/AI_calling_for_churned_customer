# predictor/views.py
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path
import pandas as pd

from .predictor import ChurnPredictor

DATA_DIR = Path(settings.BASE_DIR) / "real_time_data"

def topk_api(request):
    # Allow both GET and POST
    if request.method not in ["GET", "POST"]:
        return JsonResponse({"error": "GET/POST only"}, status=405)

    try:
        profile = pd.read_csv(DATA_DIR / "customer_profile_test.csv")
        purchase = pd.read_csv(DATA_DIR / "purchase_behavior_test.csv")
        support = pd.read_csv(DATA_DIR / "customer_support_test.csv")

        predictor = ChurnPredictor()
        topk = predictor.predict_top_k(profile, purchase, support)

        return JsonResponse({"results": topk.to_dict(orient="records")})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


## uncomment the below part to check the backend without POST

# def topk_api(request):
#     try:
#         profile = pd.read_csv(DATA_DIR / "customer_profile_test.csv")
#         purchase = pd.read_csv(DATA_DIR / "purchase_behavior_test.csv")
#         support = pd.read_csv(DATA_DIR / "customer_support_test.csv")

#         predictor = ChurnPredictor()
#         topk = predictor.predict_top_k(profile, purchase, support)

#         return JsonResponse({"results": topk.to_dict(orient="records")})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)