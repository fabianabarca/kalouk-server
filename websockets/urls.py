from django.urls import path
from . import views

urlpatterns = [
    path("", views.ws, name="ws"),
    path("test/", views.ws_test, name="ws_test"),
]
