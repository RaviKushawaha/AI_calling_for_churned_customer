from django.urls import path
from .views import topk_api, call_script_api
from .vapi_trigger_call_view import trigger_vapi_call


urlpatterns = [
    path("topk/", topk_api, name="topk_api"),
    path('call_script/', call_script_api, name='call_script_api'),
    path("api/trigger-call/", trigger_vapi_call, name="trigger_vapi_call"),

]
