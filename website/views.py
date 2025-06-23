from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")


def ws_test(request):
    return render(request, "ws_test.html")


def sse_test(request):
    return render(request, "sse_test.html")
