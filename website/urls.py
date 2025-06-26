from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("websocket/", views.ws_test, name="ws_test"),
    path("server-sent-events/", views.sse_test, name="sse_test"),
]
