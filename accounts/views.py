from django.shortcuts import render


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserPreferences, Favorite


@login_required
def profile(request):
    preference = UserPreferences.objects.filter(user=request.user).first()

    context = {
        "preference": preference
    }

    return render(request, "accounts/profile.html", context)


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)

    return render(request, "accounts/favorite_list.html", {
        "favorites": favorites
    })
