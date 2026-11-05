from datetime import timedelta

from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from accounts.models import UserPreferences
from .ai_ratings import RatingServiceError, rate_apartment_fit
from .models import Apartment, RoomPriceHistory


def home(request):
    return render(request, "home.html")


def apartment_list(request):
    apartments = Apartment.objects.prefetch_related("rooms").all()
    return render(request, "apartments/apartment_list.html", {"apartments": apartments})


def apartment_detail(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    year_ago = timezone.localdate() - timedelta(days=365)
    recent_prices = RoomPriceHistory.objects.filter(
        effective_date__gte=year_ago,
        effective_date__lte=timezone.localdate(),
    ).order_by("effective_date")
    rooms = apartment.rooms.prefetch_related(
        Prefetch("price_history", queryset=recent_prices, to_attr="recent_price_history")
    )
    preferences = (
        UserPreferences.objects.filter(user=request.user).first()
        if request.user.is_authenticated
        else None
    )
    has_rating_preferences = bool(
        preferences
        and preferences.budget is not None
        and preferences.rent_control_preference
    )
    return render(
        request,
        "apartments/apartment_detail.html",
        {
            "apartment": apartment,
            "rooms": rooms,
            "lease_records": apartment.leaserecord_set.prefetch_related("apartmentcost_set"),
            "predictions": apartment.rentprediction_set.all(),
            "has_rating_preferences": has_rating_preferences,
        },
    )


@login_required
@require_POST
def apartment_rating(request, apartment_id):
    apartment = get_object_or_404(Apartment, pk=apartment_id)
    preferences = UserPreferences.objects.filter(user=request.user).first()
    if (
        not preferences
        or preferences.budget is None
        or not preferences.rent_control_preference
    ):
        return JsonResponse(
            {
                "error": "Add your budget and rent-control preference to your profile first.",
                "profile_url": "/profile/",
            },
            status=400,
        )

    user_context = request.POST.get("context", "").strip()
    if len(user_context) > 500:
        return JsonResponse({"error": "Additional context must be 500 characters or fewer."}, status=400)

    try:
        result = rate_apartment_fit(apartment, preferences, user_context)
    except RatingServiceError as exc:
        return JsonResponse(
            {
                "error": (
                    "Local AI ratings are unavailable. Ensure Ollama is running "
                    "and the configured model is installed."
                )
            },
            status=502,
        )

    return JsonResponse(result)


def apartment_list_api(request):
    if request.method != "GET":
        response = JsonResponse({"error": "Only GET is supported."}, status=405)
        response["Allow"] = "GET"
        return response

    today = timezone.localdate()
    year_ago = today - timedelta(days=365)
    recent_prices = RoomPriceHistory.objects.filter(
        effective_date__gte=year_ago,
        effective_date__lte=today,
    ).order_by("effective_date")
    apartments = Apartment.objects.prefetch_related(
        Prefetch("rooms__price_history", queryset=recent_prices, to_attr="recent_price_history")
    ).order_by("id")
    data = []
    for apartment in apartments:
        rooms = []
        for room in apartment.rooms.all():
            rooms.append(
                {
                    "id": room.id,
                    "unit_number": room.unit_number,
                    "bedroom_count": room.bedroom_count,
                    "bathroom_count": str(room.bathroom_count),
                    "square_footage": room.square_footage,
                    "current_monthly_rent": str(room.current_monthly_rent),
                    "max_occupancy": room.max_occupancy,
                    "current_occupants": room.current_occupants,
                    "price_history": [
                        {
                            "effective_date": price.effective_date.isoformat(),
                            "monthly_rent": str(price.monthly_rent),
                        }
                        for price in room.recent_price_history
                    ],
                }
            )
        data.append(
            {
                "id": apartment.id,
                "name": apartment.name,
                "average_rating": str(apartment.average_rating),
                "street_address": apartment.street_address,
                "city": apartment.city,
                "zip_code": apartment.zip_code,
                "rent_controlled": apartment.rent_controlled,
                "rooms": rooms,
            }
        )

    return JsonResponse({"apartments": data})
