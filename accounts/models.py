from django.db import models
from django.contrib.auth.models import User
from apartments.models import Apartment


class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=8, decimal_places=2)
    min_bedrooms = models.PositiveIntegerField()
    min_bathrooms = models.PositiveIntegerField()
    preferred_location = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'apartment'],
                name="unique_user_apartment_favorite"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.apartment.name}"