from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")


def ws(request):
    return render(request, "ws.html")


def sse(request):
    return render(request, "sse.html")
