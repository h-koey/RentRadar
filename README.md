# Illini Rent Radar: Are You Paying Too Much?

### A smarter way for University of Illinois students to compare off-campus housing costs

Make more informed housing decisions by comparing historical apartment rents, estimating additional expenses, and exploring future rental trends.

**Project:** Illini Rent Radar  
**Team:** 20

[![Python](https://img.shields.io/badge/Python-324841?logo=python&logoColor=white)](https://www.python.org/) 
[![Django](https://img.shields.io/badge/Django-324841?logo=django&logoColor=white)](https://www.djangoproject.com/) 
[![AI](https://img.shields.io/badge/AI-In%20Development-ADC2AF)](#features)
![License](https://img.shields.io/badge/License-Apache%202.0-9C95C9)

[Quick Guide](#quick-guide) | [Planned Features](#planned-features) | [Run the App](#run-the-app) | [Project Status](#project-status) | [Team](#team)

---

## Quick Guide

1. **Explore the project:** Learn about our goals and planned features below.
2. **Run the application:** Follow the [Run the App](#run-the-app) instructions.
3. **Learn about the AI feature:** See the AI documentation once available.

## Overview

Illini Rent Radar is a web application designed to help University of Illinois Urbana-Champaign students and Champaign-Urbana community members make informed off-campus housing decisions.

The application aims to help users compare historical rental prices, understand additional housing costs and fees, and estimate future rent and utility expenses.

## The Problem

Finding affordable off-campus housing can be challenging. Advertised rent may not include additional expenses such as utilities, parking, application fees, and amenity fees. These extra costs make it difficult for renters to compare apartments and plan their budgets accurately.

Illini Rent Radar aims to make these expenses easier to understand and housing options easier to compare.

## Planned Features

The following features are planned and currently under development.

### 🏠 Apartment Lease Search

- Search historical apartment lease information.
- Filter by location, price, bedroom and bathroom count, and lease year.
- Compare rental information to make more informed housing decisions.

### 💰 Total Housing Cost Calculator

- Combine rent, estimated utilities, and additional fees.
- Customize expenses to reflect individual housing situations.
- Calculate estimated monthly and yearly housing costs.

### 🤖 Rent Trends and Predictions

- Visualize historical rental price changes.
- Explore estimated future rent costs.
- Use historical rental information and AI or statistical techniques to support rent predictions.

## Technology

- **Python:** Primary programming language.
- **Django:** Web application framework.
- **SQLite:** Database currently used for storing application data.
- **Django ORM:** Manages database models and queries.
- **HTML and CSS:** User interface and styling.
- **AI / Statistical Techniques:** Being explored for rent prediction and trend analysis.

Technology choices may be updated as development progresses.

## Run the App

### 1. Clone the repository

```sh
git clone https://github.com/h-koey/RentRadar.git
cd RentRadar
```

### 2. Create and activate a virtual environment

```sh
python -m venv .venv
```

**Mac/Linux:**

```sh
source .venv/bin/activate
```

**Windows:**

```sh
.venv\Scripts\activate
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure the Django secret key

1. Copy `.env.example` to `.env` in the project folder (the same folder as `manage.py`).
2. Generate a new key:

```sh
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

3. Put the generated value after `DJANGO_SECRET_KEY=` in `.env`.
4. Keep `.env` private. It is ignored by Git and should never be committed.

### 5. Run database migrations

```sh
python manage.py migrate
```

### 6. Start the development server

```sh
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

*Note: Setup instructions should be verified against the team's current Django configuration.*

## Project Status

The project is currently in its initial development stage. The team is working on the Django application foundation, database functionality, AI implementation, testing, and deployment planning.

### Development Progress

- **10/25:** Completed initial project proposal and wireframes. Created GitHub repository.
- **10/28:** Established team responsibilities and organized the initial README structure.
- **11/04:** Created initial Django models, views, URLs, and templates; pushed changes to GitHub.
- **11/05:** Set up the SQLite database.
- **11/06:** Began evaluating AI models and testing metrics. Started deployment cost analysis and planning.

### Currently In Progress

- Completing Django application functionality and authorization.
- Developing database and API functionality.
- Evaluating models for the rent prediction feature.
- Testing model performance and response quality.
- Planning deployment, hosting costs, and production requirements.
- Updating project documentation and setup instructions.

The application and its planned features are still under development.

## Project Documentation

Additional documentation will be added as development progresses.

| Document | Description |
|---|---|
| `README_AI.md` | AI implementation, model/technique, predictions, and evaluation |
| `docs/project_scope.md` | Updated project scope and planned features |
| `docs/development_roadmap.md` | Development tasks, team responsibilities, and expected completion dates |
| `docs/testing_and_evaluation.md` | Testing results, limitations, and improvements |

## Team

**Team 20** — University of Illinois Urbana-Champaign

*Members: Koey Huang, Marley Karsen, Nick Rondon, Henry Rotunno*

## Disclaimer

Future rent and utility values are estimates and may differ from actual housing costs. This application is intended as a reference to support housing decisions, not as a guarantee of exact costs.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
