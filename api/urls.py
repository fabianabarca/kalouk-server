from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"datos", views.DataViewSet, basename="datos")
router.register(r"proceso", views.DataViewSet, basename="proceso")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls), name="api-root"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
