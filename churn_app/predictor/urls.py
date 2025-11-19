from django.urls import path
from .views import topk_api

urlpatterns = [
    path("topk/", topk_api, name="topk_api"),
]
