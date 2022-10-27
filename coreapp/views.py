from django.http import HttpResponse
from django.http import HttpResponse


def IndexView(request):
    """Root url, nothing happens but : say Hello to grandma!"""
    return HttpResponse( "say Hello to Power Factors!!")
