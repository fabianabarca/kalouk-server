from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/$", consumers.SlidevSyncConsumer.as_asgi()),
    re_path(r"^ws/test/$", consumers.TestConsumer.as_asgi()),
    re_path(
        r"^ws/deck/slider/(?P<deck_id>\w+)/$", consumers.DeckSliderConsumer.as_asgi()
    ),
]
