import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")
VAPI_PHONE_NUMBER_ID = os.getenv("VAPI_PHONE_NUMBER_ID")

VAPI_CALL_URL = "https://api.vapi.ai/call"


@csrf_exempt
def trigger_vapi_call(request):
    """
    POST /api/trigger-call/

    Body JSON:
    {
      "phone": "+918354035993",
      "script": "Hi there ..."
    }
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    if not (VAPI_API_KEY and VAPI_ASSISTANT_ID and VAPI_PHONE_NUMBER_ID):
        return JsonResponse(
            {"error": "VAPI env vars missing (VAPI_API_KEY, VAPI_ASSISTANT_ID, VAPI_PHONE_NUMBER_ID)"},
            status=500,
        )

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    phone = data.get("phone")
    script = data.get("script")

    if not phone or not script:
        return JsonResponse({"error": "phone and script are required"}, status=400)

    payload = {
        "assistantId": VAPI_ASSISTANT_ID,
        "phoneNumberId": VAPI_PHONE_NUMBER_ID,
        "customer": {
            "number": phone
        },
        "metadata": {
            "script": script
        },
    }

    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(VAPI_CALL_URL, headers=headers, json=payload, timeout=15)
    except Exception as e:
        return JsonResponse({"error": f"Failed to reach Vapi: {e}"}, status=502)

    if not resp.ok:
        return JsonResponse(
            {"error": "Vapi call failed", "status": resp.status_code, "body": resp.text},
            status=502,
        )

    return JsonResponse(resp.json())
