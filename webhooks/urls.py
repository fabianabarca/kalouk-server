from django.urls import path
from . import views

urlpatterns = [
    path("", views.webhooks, name="webhooks"),
    path("test/", views.test, name="test_webhook"),
    path("github/", views.github, name="github_webhook"),
    path("kalouk/", views.kalouk, name="kalouk_webhook"),
]
