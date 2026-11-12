from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.decorators.http import require_http_methods

from .forms import RegistrationForm, UserPreferencesForm
from .models import Favorite, UserPreferences


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("profile")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("profile")

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    preference = UserPreferences.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = UserPreferencesForm(request.POST, instance=preference)
        if form.is_valid():
            preference = form.save(commit=False)
            preference.user = request.user
            preference.save()
            return redirect("profile")
    else:
        form = UserPreferencesForm(instance=preference)

    context = {
        "preference": preference,
        "form": form,
    }

    return render(request, "accounts/profile.html", context)


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("apartment")
    return render(request, "accounts/favorite_list.html", {"favorites": favorites})
