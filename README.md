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
- 10/25: Completed initial proposal + wireframes, GitHub repository launched.
- 10/28: Discussed split of responsibility. Plans: Django development, database functionality, AI integration, and testing will be implemented (draft-level)
## Setup Instructions / How to Run Locally
IP
## Disclaimer
Future rent & utility values are estimates. May differ from actual housing costs. This application is a reference, not an exact truth.

