from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from apartments.models import Apartment, Room, RoomPriceHistory


class Command(BaseCommand):
    help = "Add two sample apartment listings and one year of room rent history."

    def handle(self, *args, **options):
        listings = [
            {
                "name": "Sample Green Apartments",
                "street_address": "101 Green Street",
                "city": "Champaign",
                "zip_code": "61820",
                "average_rating": Decimal("4.30"),
                "rent_controlled": False,
                "room": {
                    "unit_number": "2A",
                    "bedroom_count": 2,
                    "bathroom_count": Decimal("1.0"),
                    "square_footage": 850,
                    "current_monthly_rent": Decimal("1450.00"),
                    "max_occupancy": 3,
                    "current_occupants": 2,
                },
                "rent_start": Decimal("1330.00"),
            },
            {
                "name": "Sample Urbana Lofts",
                "street_address": "220 Main Street",
                "city": "Urbana",
                "zip_code": "61801",
                "average_rating": Decimal("4.65"),
                "rent_controlled": True,
                "room": {
                    "unit_number": "304",
                    "bedroom_count": 1,
                    "bathroom_count": Decimal("1.0"),
                    "square_footage": 620,
                    "current_monthly_rent": Decimal("1125.00"),
                    "max_occupancy": 2,
                    "current_occupants": 0,
                },
                "rent_start": Decimal("1050.00"),
            },
        ]

        today = timezone.localdate()
        for listing in listings:
            room_data = listing["room"]
            rent_start = listing["rent_start"]
            apartment, _ = Apartment.objects.get_or_create(
                name=listing["name"],
                street_address=listing["street_address"],
                defaults={
                    "city": listing["city"],
                    "zip_code": listing["zip_code"],
                    "average_rating": listing["average_rating"],
                    "rent_controlled": listing["rent_controlled"],
                },
            )
            room, _ = Room.objects.get_or_create(
                apartment=apartment,
                unit_number=room_data["unit_number"],
                defaults=room_data,
            )

            for month_ago in range(12, -1, -1):
                effective_date = today - timedelta(days=30 * month_ago)
                monthly_rent = min(
                    rent_start + Decimal("10.00") * (12 - month_ago),
                    room.current_monthly_rent,
                )
                RoomPriceHistory.objects.get_or_create(
                    room=room,
                    effective_date=effective_date,
                    defaults={"monthly_rent": monthly_rent},
                )

            self.stdout.write(f"Ready: {apartment.name} (ID {apartment.pk})")
