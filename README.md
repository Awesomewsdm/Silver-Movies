# Silver Movies (Project Nexus)

Silver Movies is a movie recommendation backend built with Django REST Framework. It integrates with The Movie Database (TMDb) API to provide trending movies and recommendations, supports user authentication with JWT, and allows users to save favorite movies. The project is containerized with Docker and designed for deployment to platforms like Render.

## Table of Contents

- [Features](#features)
- [Live demo](#live-demo)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting started (local development)](#getting-started-local-development)
- [Environment variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Postman](#postman)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Next steps / Enhancements](#next-steps--enhancements)
- [License](#license)

## Features

- REST API endpoints for trending movies, recommendations, and user favorites
- JWT authentication with registration and token refresh
- Redis caching for TMDb responses to reduce latency and external calls
- PostgreSQL database with Django ORM models and migrations
- Swagger/OpenAPI documentation via `drf-yasg` at `/api/docs/`
- Dockerized for development and production (Gunicorn for WSGI)
- CI workflow for running tests and building images
- A Postman collection for quick manual testing

## Live demo

- Base URL: `https://silver-movies.onrender.com`
- Swagger UI: `https://silver-movies.onrender.com/api/docs/`

## Tech Stack

- Python 3.10
- Django 4.x
- Django REST Framework
- PostgreSQL
- Redis
- Docker & Docker Compose
- Gunicorn
- drf-yasg (Swagger)
- djangorestframework-simplejwt (JWT)
- Requests (TMDb client)

## Project Structure

- `project_nexus/` — Django project
  - `project_nexus/settings.py` — Django settings
  - `project_nexus/urls.py` — root URL config (includes API docs)
- `project_nexus/movies/` — `movies` app
  - `models.py` — `FavoriteMovie` model
  - `serializers.py` — DRF serializers
  - `views.py` — API views (health, auth register/me, trending, recommendations, favorites)
  - `tmdb.py` — TMDb client with retries and caching
  - `tests/` — unit tests for client and views
- `Dockerfile` — production image with Gunicorn
- `docker-compose.yml` — development services (db, redis, web)
- `docker-compose.prod.yml` — production compose (optional)
- `requirements.txt` — Python dependencies
- `postman/` — Postman collection (`silver-movies.postman_collection.json`)
- `README_DEPLOY.md` — deployment notes and Render instructions

## Getting started (local development)

Prerequisites: Docker & Docker Compose, or Python 3.10 and a virtual environment.

Using Docker (recommended):

```bash
# build and run services
docker compose up --build -d db redis
# run web (migrations will be needed)
docker compose run --rm web python project_nexus/manage.py migrate
docker compose up -d
# create a superuser if needed
docker compose run --rm web python project_nexus/manage.py createsuperuser
```

Using virtualenv (without Docker):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DJANGO_DEBUG=True
export POSTGRES_DB=silver_movies
# configure a running Postgres instance locally
python project_nexus/manage.py migrate
python project_nexus/manage.py runserver
```

## Environment variables

Example `.env` (development):

```dotenv
DJANGO_SECRET_KEY=dev-secret-key
DJANGO_DEBUG=True
POSTGRES_DB=silver_movies
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
TMDB_API_KEY=your_tmdb_api_key_here
REDIS_URL=redis://redis:6379/0
```

In production, set `DJANGO_DEBUG=False` and provide `DATABASE_URL` (Render Postgres supplies this automatically when you attach a managed DB).

## API Endpoints

- `GET /api/health/` — Health check
- `POST /api/auth/register/` — Register user (returns JWT tokens)
- `POST /api/auth/token/` — Obtain tokens
- `POST /api/auth/token/refresh/` — Refresh access token
- `GET /api/auth/me/` — Get current user (requires auth)
- `GET /api/movies/trending/` — Trending movies (TMDb)
- `GET /api/movies/<tmdb_id>/recommendations/` — Movie recommendations
- `GET/POST /api/favorites/` — List and create favorites (requires auth)
- `DELETE /api/favorites/<id>/` — Delete a favorite (requires auth)

See `README_DEPLOY.md` for deployment-specific instructions and the Postman collection.

## Testing

Run Django tests locally:

```bash
docker compose run --rm web python project_nexus/manage.py test
```

## Postman

Import the collection at `postman/silver-movies.postman_collection.json`. Update the `base_url` variable to point to your deployed URL (e.g., `https://silver-movies.onrender.com`). The collection includes scripts to capture `access_token` and `refresh_token` after registration or token obtain.

## Deployment

See `README_DEPLOY.md` for Render deployment steps, env vars, release commands, and health checks.

## Contributing

- Fork the repository and create a topic branch for your change.
- Open a pull request with a clear description and include tests for new functionality.
- Keep changes focused and follow existing code style.

## Next steps / Enhancements

- Add GraphQL option (using `graphene-django`) if you want a GraphQL API alongside REST.
- Add Celery for background tasks (cache warming, scheduled jobs) when needed.
- Integrate Sentry for error monitoring and add automated DB backups.
- Improve test coverage and add an E2E smoke test step in CI that hits the deployed URL.

## License

This project is for learning / portfolio purposes. Add license details if you intend to publish publicly.# Silver Movies (Project Nexus)

Backend for a movie recommendation application using Django REST Framework.

See `README_DEV.md` for development instructions.

See `README_DEPLOY.md` for deployment and production setup instructions (Render, env vars, health checks, endpoints).
