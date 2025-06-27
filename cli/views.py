from django.shortcuts import render

# Create your views here.


def cli(request):
    """
    Render the CLI interface.
    """
    return render(request, "cli.html")
