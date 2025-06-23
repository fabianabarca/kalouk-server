from django.shortcuts import render

# Create your views here.


def ws(request):
    return render(request, "ws.html")


def ws_test(request):
    return render(request, "ws_test.html")
