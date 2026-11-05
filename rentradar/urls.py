"""
URL configuration for radar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from apartments import views as apartment_views
from accounts import views as account_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", apartment_views.home, name="home"),

    # Apartment pages
    path("apartments/", apartment_views.apartment_list, name="apartment_list"),
    path("apartments/<int:apartment_id>/", apartment_views.apartment_detail, name="apartment_detail"),
    path("apartments/<int:apartment_id>/rate/", apartment_views.apartment_rating, name="apartment_rating"),
    path("api/apartments/", apartment_views.apartment_list_api, name="apartment_list_api"),

    # Account pages
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("accounts/register/", account_views.register, name="register"),
    path("profile/", account_views.profile, name="profile"),
    path("favorites/", account_views.favorite_list, name="favorite_list"),


    path('accounts/', include('allauth.urls')),
]