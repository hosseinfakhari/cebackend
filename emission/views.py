from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def testapi(request):
    return HttpResponse("api test")
