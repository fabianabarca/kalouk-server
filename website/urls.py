from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ws-test/", views.ws, name="ws_test"),
    path("sse-test/", views.sse, name="sse_test"),
]
