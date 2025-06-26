from django.shortcuts import render
from decouple import config

# Create your views here.


def index(request):
    return render(request, "index.html")


def ws_test(request):
    websocket = config("WEBSOCKET", default="http://localhost:8000/sse/")
    context = {
        "websocket": websocket,
    }
    return render(request, "ws_test.html", context)


def sse_test(request):
    event_source = config("EVENT_SOURCE", default="http://localhost:8000/sse/")
    context = {
        "event_source": event_source,
    }
    return render(request, "sse_test.html", context)
