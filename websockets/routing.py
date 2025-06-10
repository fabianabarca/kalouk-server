from django.urls import re_path

from .consumers import TestConsumer, DeckSliderConsumer

websocket_urlpatterns = [
    re_path(r"^ws/test/$", TestConsumer.as_asgi()),
    re_path(r"^ws/deck/slider/(?P<deck_id>\w+)/$", DeckSliderConsumer.as_asgi()),
]
