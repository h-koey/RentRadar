from django.db import transaction
from django.utils import timezone

from .models import Apartment, Room, RoomPriceHistory


@transaction.atomic
def add_apartment(
    *,
    name,
    street_address,
    city,
    zip_code,
    first_room,
    average_rating=0,
    rent_controlled=False,
):
    apartment = Apartment(
        name=name,
        street_address=street_address,
        city=city,
        zip_code=zip_code,
        average_rating=average_rating,
        rent_controlled=rent_controlled,
    )
    apartment.full_clean()
    apartment.save()
    add_room(apartment, **first_room)
    return apartment


@transaction.atomic
def add_room(apartment, **room_data):
    if not isinstance(apartment, Apartment):
        apartment = Apartment.objects.get(pk=apartment)
    elif apartment.pk is None:
        raise ValueError("Save the apartment before adding a room.")

    room = Room(apartment=apartment, **room_data)
    room.save()
    RoomPriceHistory.objects.create(
        room=room,
        effective_date=timezone.localdate(),
        monthly_rent=room.current_monthly_rent,
    )
    return room
