import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

RETELL_API_KEY = os.getenv("RETELL_API_KEY")
RETELL_AGENT_ID = os.getenv("RETELL_AGENT_ID")  # your Retell agent / bot id

RETELL_CALL_URL = "https://api.retellai.com/v1/calls"  # example endpoint


@csrf_exempt
def trigger_retell_call(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    if not (RETELL_API_KEY and RETELL_AGENT_ID):
        return JsonResponse(
            {"error": "RETELL_API_KEY or RETELL_AGENT_ID missing in env"},
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
        "agent_id": RETELL_AGENT_ID,
        "phone_number": phone,
        "metadata": {
            "script": script,
        },
    }

    headers = {
        "Authorization": f"Bearer {RETELL_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(RETELL_CALL_URL, json=payload, headers=headers, timeout=15)
    except Exception as e:
        return JsonResponse({"error": f"Failed to reach Retell: {e}"}, status=502)

    if not resp.ok:
        return JsonResponse(
            {"error": "Retell call failed", "status": resp.status_code, "body": resp.text},
            status=502,
        )

    return JsonResponse(resp.json())
