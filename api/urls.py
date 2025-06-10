from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("datos/", views.DataView.as_view(), name="datos"),
    path("proceso/", views.ProcessView.as_view(), name="proceso"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
