from idlelib.help import copy_strip

from django.shortcuts import render, get_object_or_404

from django.shortcuts import render
from .models import Apartment


def home(request):
    return render(request, "home.html")


def apartment_list(request):
    apartments = Apartment.objects.all()

    context = {
        "apartments": apartments
    }

    return render(request, "apartments/apartment_list.html", context)


def apartment_detail(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)

    context = {
        "apartment": apartment,
        "lease_records": apartment.lease_records.all(),
        "costs": [
            cost
            for lease in apartment.lease_records.all()
            for cost in lease.costs.all()
        ],
        "predictions": apartment.predictions.all()
    }

    return render(request, "apartments/apartment_detail.html", context)

