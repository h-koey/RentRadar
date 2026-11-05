from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.utils import timezone


class Apartment(models.Model):
    name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rent_controlled = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(average_rating__gte=0, average_rating__lte=5),
                name="apartment_rating_0_to_5",
            ),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.pk:
            if not self.rooms.exists():
                raise ValidationError("An apartment must have at least one room.")
            if not self.rooms.filter(current_occupants__lt=F("max_occupancy")).exists():
                raise ValidationError("An apartment must have at least one vacant room.")


class LeaseRecord(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=20)
    lease_year = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2)
    lease_term_months = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.apartment} - Unit {self.unit_number} - {self.lease_year}"


class Room(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="rooms")
    unit_number = models.CharField(max_length=20)
    bedroom_count = models.PositiveIntegerField()
    bathroom_count = models.DecimalField(max_digits=3, decimal_places=1)
    square_footage = models.PositiveIntegerField()
    current_monthly_rent = models.DecimalField(max_digits=8, decimal_places=2)
    max_occupancy = models.PositiveIntegerField()
    current_occupants = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["apartment", "unit_number"],
                name="unique_room_number_per_apartment",
            ),
            models.CheckConstraint(
                condition=models.Q(max_occupancy__gt=0),
                name="room_max_occupancy_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(current_occupants__lte=F("max_occupancy")),
                name="room_occupants_not_over_capacity",
            ),
            models.CheckConstraint(
                condition=models.Q(current_monthly_rent__gte=0),
                name="room_rent_nonnegative",
            ),
            models.CheckConstraint(
                condition=models.Q(square_footage__gt=0),
                name="room_square_footage_positive",
            ),
        ]

    def clean(self):
        super().clean()
        if (
            self.apartment_id
            and self.max_occupancy
            and self.current_occupants < self.max_occupancy
        ):
            return
        if self.apartment_id:
            vacant_sibling = Room.objects.filter(
                apartment_id=self.apartment_id,
                current_occupants__lt=F("max_occupancy"),
            ).exclude(pk=self.pk)
            if not vacant_sibling.exists():
                raise ValidationError(
                    "Each apartment must have at least one vacant room."
                )

    def __str__(self):
        return f"{self.apartment.name} - Room {self.unit_number}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class RoomPriceHistory(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="price_history")
    effective_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ["effective_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["room", "effective_date"],
                name="unique_room_price_on_date",
            ),
            models.CheckConstraint(
                condition=models.Q(monthly_rent__gte=0),
                name="room_price_history_nonnegative",
            ),
        ]

    @classmethod
    def for_past_year(cls, room):
        today = timezone.localdate()
        return cls.objects.filter(
            room=room,
            effective_date__gte=today - timedelta(days=365),
            effective_date__lte=today,
        )

    def __str__(self):
        return f"{self.room} - {self.effective_date}: ${self.monthly_rent}"


class ApartmentCost(models.Model):
    COST_TYPES = [
        ("utility", "Utility"),
        ("parking", "Parking"),
        ("application", "Application"),
        ("service", "Service"),
        ("other", "Other"),
    ]

    FREQUENCIES = [
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
        ("one_time", "One Time"),
    ]

    lease_record = models.ForeignKey(LeaseRecord, on_delete=models.CASCADE)
    cost_type = models.CharField(max_length=20, choices=COST_TYPES)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=FREQUENCIES)

    def __str__(self):
        return f"{self.name}: ${self.amount}"


class RentPrediction(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    target_year = models.PositiveIntegerField()
    estimated_monthly_rent = models.DecimalField(max_digits=8, decimal_places=2)
    estimated_monthly_utilities = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["target_year"]

    def __str__(self):
        return f"{self.apartment.name} - Prediction for {self.target_year}"


class Room(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="rooms")
    unit_number = models.CharField(max_length=20)
    bedroom_count = models.PositiveIntegerField()
    bathroom_count = models.DecimalField(max_digits=3, decimal_places=1)
    square_footage = models.PositiveIntegerField()
    current_monthly_rent = models.DecimalField(max_digits=8, decimal_places=2)
    max_occupancy = models.PositiveIntegerField()
    current_occupants = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["apartment", "unit_number"], name="unique_room_number_per_apartment"),
            models.CheckConstraint(condition=models.Q(max_occupancy__gt=0), name="room_max_occupancy_positive"),
            models.CheckConstraint(condition=models.Q(current_occupants__lte=F("max_occupancy")), name="room_occupants_not_over_capacity"),
            models.CheckConstraint(condition=models.Q(current_monthly_rent__gte=0), name="room_rent_nonnegative"),
            models.CheckConstraint(condition=models.Q(square_footage__gt=0), name="room_square_footage_positive"),
        ]

    def clean(self):
        super().clean()
        if self.apartment_id and self.max_occupancy and self.current_occupants < self.max_occupancy:
            return
        if self.apartment_id:
            vacant_sibling = Room.objects.filter(
                apartment_id=self.apartment_id,
                current_occupants__lt=F("max_occupancy"),
            ).exclude(pk=self.pk)
            if not vacant_sibling.exists():
                raise ValidationError("Each apartment must have at least one vacant room.")

    def __str__(self):
        return f"{self.apartment.name} - Room {self.unit_number}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class RoomPriceHistory(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="price_history")
    effective_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ["effective_date"]
        constraints = [
            models.UniqueConstraint(fields=["room", "effective_date"], name="unique_room_price_on_date"),
            models.CheckConstraint(condition=models.Q(monthly_rent__gte=0), name="room_price_history_nonnegative"),
        ]

    def __str__(self):
        return f"{self.room} - ${self.monthly_rent} on {self.effective_date}"
