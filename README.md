# 20-rentradar

## Updating the Django secret key

1. Copy `.env.example` to `.env` in the project folder (the same folder as `manage.py`).
2. Generate a new key with:

   ```sh
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. Put the generated value after `DJANGO_SECRET_KEY=` in `.env`.
4. Keep `.env` private. It is ignored by Git, so don't add it to a commit.
___________________________________________________________________________________________________________
___________________________________________________________________________________________________________
# Illini Rent Radar
- Project: `Illini Rent Radar` 
- Team: 20
- Members: Koey Huang*, Marley Karsen*, Nick Rondon*, Henry Rotunno*

## Overview
Illini Rent Radar is a web application designed to help University of Illinois Urbana-Champaign students and Urbana-Champaign community members make informed off-campus housing decisions. 
This application aims to help users compare historical prices, understand additional housing costs & fees, and project future rent and utility costs.
## Problem
Finding affordable off-campus housing can be challenging. Advertised rent may not include additional expenses such as utilities, parking, application fees, and amenity fees; this makes it difficult to budget accordingly. Illini Rent Radar aims to help users understand these costs and compare apartments in a more effective manner.
## Planned Core Features
1. **Lease Search:** Search historical apartment lease information. Use filters like price, bedroom & bathroom count, and lease year for specific detailing.
2. **Total Cost Calculator:** Combines rent, estimated utilities, and other fees (can freely customize) to calculate (generally) monthly and yearly housing costs.
3. **Rent Trends & Predictions:** Visualize historical rent changes. Explore estimated future rent costs.
## Technology
- Python
- Django
- Database & Django ORM
- HTML & CSS
- AI / other statistical techniques for rent prediction feature
Technology choices will be updated as development progresses.
## Project Status
- 10/25: Completed initial proposal + wireframes. Created GitHub repository.
- 10/28: Discussed team responsibilities and plans for Django development, database functionality, AI integration, and testing.
## Apartment listings

The apartment listing page is available at `/apartments/`. A JSON read API is
available at `GET /api/apartments/`; it returns apartments, rooms, and each
room's price history from the past year.

To load two repeatable sample listings with room and rent history data, run:

```sh
python manage.py seed_demo_listings
```

In Python code, use `apartments.services.add_apartment(...)` to create an
apartment together with its first room, or
`apartments.services.add_room(apartment, ...)` to add a room to an existing
apartment. `apartment` can be either an `Apartment` instance or its database ID.

## Personalized AI apartment ratings

Install [Ollama](https://ollama.com/download) and download a local model that
supports JSON output, for example:

```sh
ollama pull llama3.1
```

When started with `python manage.py runserver`, the app starts Ollama's local
server if it is not already running. Ollama must be installed; if its executable
is not on `PATH` or in a standard install location, set `OLLAMA_EXECUTABLE` in
the project-root `.env` file to its full path (for example,
`C:\Users\your-name\AppData\Local\Programs\Ollama\ollama.exe`). If startup fails,
the web app still starts, but AI ratings remain unavailable until Ollama is
running. The app connects to `http://localhost:11434/api/chat` by default. Set
`OLLAMA_BASE_URL` or `OLLAMA_MODEL` in `.env` to use a different local server or
installed model; the defaults are `http://localhost:11434` and `llama3.1`.
Users can save their monthly budget and rent-control preference from **My Profile**.
On an apartment detail page, users with those preferences can request an AI score
for the apartment and its rooms, with optional additional context. Ratings are
generated on demand and are not saved to the database. If the required profile
preferences are missing, the page links to the profile form instead.

Users can create an account at `/accounts/register/` with a username and password.
Registration also accepts an optional email address and signs the user in after
the account is created.
## Disclaimer
Future rent & utility values are estimates. May differ from actual housing costs. This application is intended as a reference to support housing decisions, not as a guarantee of exact costs.
