from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ws-test/", views.ws_test, name="ws_test"),
    path("sse-test/", views.sse_test, name="sse_test"),
]
