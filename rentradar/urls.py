from django.contrib import admin
from django.urls import path
from apartments import views as apartment_views
from accounts import views as account_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", apartment_views.home, name="home"),

    # Apartment pages
    path("apartments/", apartment_views.apartment_list, name="apartment_list"),
    path("apartments/<int:apartment_id>/", apartment_views.apartment_detail, name="apartment_detail"),

    # Account pages
    path("profile/", account_views.profile, name="profile"),
    path("favorites/", account_views.favorite_list, name="favorite_list"),
]