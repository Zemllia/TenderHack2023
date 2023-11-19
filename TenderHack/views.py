from django.http import HttpResponse
from django.shortcuts import render

from TenderHack.models import Subdivision


def index(request):
    return HttpResponse(render(request, "site/index.html", context={
        "subdivisions_count": Subdivision.objects.filter(is_supplier=True).count()
    }))


def comparsion(request):
    return HttpResponse(render(request, "site/comparsion.html", context={
        "subdivisions_count": Subdivision.objects.filter(is_supplier=True).count()
    }))


