from django.db import models


class Apartment(models.Model):
    name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5)

    def __str__(self):
        return self.name


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
