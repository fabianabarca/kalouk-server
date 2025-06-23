"""
ASGI config for kalouk project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path, re_path

from ws.routing import websocket_urlpatterns
from sse.consumers import StateSSEConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kalouk.settings")

application = ProtocolTypeRouter(
    {
        "http": URLRouter(
            [
                path("sse/", StateSSEConsumer.as_asgi()),
                path("sse", StateSSEConsumer.as_asgi()),
                re_path(r"", get_asgi_application()),
            ]
        ),
        "websocket": URLRouter(websocket_urlpatterns),
    }
)
