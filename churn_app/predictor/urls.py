from django.urls import path
from .views import topk_api, call_script_api

urlpatterns = [
    path("topk/", topk_api, name="topk_api"),
    path('call_script/', call_script_api, name='call_script_api'),
]
