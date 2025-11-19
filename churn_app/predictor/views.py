# predictor/views.py
import json
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
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

def _load_merged():
    profile = pd.read_csv(DATA_DIR / "customer_profile_test.csv")
    purchase = pd.read_csv(DATA_DIR / "purchase_behavior_test.csv")
    support = pd.read_csv(DATA_DIR / "customer_support_test.csv")
    merged = (
        profile.merge(purchase, on="customer_id")
               .merge(support, on="customer_id")
    )
    return merged


def generate_call_script(context):
    # return "Tell about your problem"
    return (
        f"Hi there, this is from Minimalist, your skincare partner.\n\n"
        f"We noticed that you've placed {context['total_orders']} orders with us, "
        f"with an average spend of around ₹{context['avg_order_value']:.0f}. "
        f"It's been about {context['days_since_last_purchase']} days since your last purchase.\n\n"
        f"Our products are designed to be gentle, effective, and transparent on ingredients, "
        f"so your skin routine stays simple and consistent.\n\n"
        f"We'd love for you to explore our latest range again — "
        f"if you have any questions or need product suggestions, we're here to help!"
    )

@csrf_exempt
def call_script_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        customer_id = data.get("customer_id")
        if customer_id is None:
            return JsonResponse({"error": "customer_id required"}, status=400)

        merged = _load_merged()
        row = merged.loc[merged["customer_id"] == customer_id]
        if row.empty:
            return JsonResponse({"error": "Customer not found"}, status=404)

        row = row.iloc[0]
        context = {
            "total_orders": int(row["total_orders"]),
            "avg_order_value": float(row["avg_order_value"]),
            "days_since_last_purchase": int(row["days_since_last_purchase"]),
        }

        script = generate_call_script(context)
        print("script:", script)

        return JsonResponse({
            "customer_id": int(row["customer_id"]),
            "phone_number": str(row["phone_number"]),
            "call_script": script,
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
